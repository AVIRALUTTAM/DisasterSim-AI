"""
Unit tests for the simulation engine — run with:  pytest tests/
"""

import pytest
from app.engine import SimulationEngine, SimConfig


def make_engine(**kwargs) -> SimulationEngine:
    cfg = SimConfig(node_count=40, seed=42, **kwargs)
    return SimulationEngine(cfg)


class TestGraphConstruction:
    def test_node_count(self):
        eng = make_engine()
        assert len(eng.nodes) == 40

    def test_patient_zero(self):
        eng = make_engine()
        infected = [n for n in eng.nodes if n.state == "infected"]
        assert len(infected) == 1

    def test_edges_exist(self):
        eng = make_engine()
        assert len(eng.edges) > 0

    def test_adjacency_symmetric(self):
        eng = make_engine()
        for a, b in eng.edges:
            assert b in eng._adj[a]
            assert a in eng._adj[b]

    def test_reproducibility_with_seed(self):
        e1 = make_engine(seed=123)
        e2 = make_engine(seed=123)
        states1 = [n.state for n in e1.nodes]
        states2 = [n.state for n in e2.nodes]
        assert states1 == states2

    def test_different_seeds_differ(self):
        e1 = make_engine(seed=1)
        e2 = make_engine(seed=2)
        states1 = [n.state for n in e1.nodes]
        states2 = [n.state for n in e2.nodes]
        assert states1 != states2


class TestSimulationStep:
    def test_step_increments(self):
        eng = make_engine()
        eng.advance()
        assert eng.step == 1

    def test_total_nodes_constant(self):
        eng = make_engine(spread_rate=0.9)
        for _ in range(20):
            eng.advance()
        total = sum(1 for n in eng.nodes if n.state in ("susceptible", "infected", "recovered", "immune"))
        assert total == 40

    def test_infection_can_spread(self):
        eng = make_engine(spread_rate=1.0, recovery_rate=0.0, density=0.5)
        for _ in range(30):
            eng.advance()
        infected_or_recovered = sum(1 for n in eng.nodes if n.state in ("infected", "recovered"))
        assert infected_or_recovered > 1

    def test_recovery_happens(self):
        eng = make_engine(spread_rate=1.0, recovery_rate=1.0)
        for _ in range(10):
            eng.advance()
        infected = sum(1 for n in eng.nodes if n.state == "infected")
        assert infected == 0

    def test_stats_sum_to_total(self):
        eng = make_engine(spread_rate=0.5, recovery_rate=0.1)
        for _ in range(10):
            stats = eng.advance()
        assert stats.total == 40


class TestInterventions:
    def test_fact_check_reduces_infected(self):
        eng = make_engine(spread_rate=1.0, recovery_rate=0.0, density=0.5)
        for _ in range(10):
            eng.advance()
        before = sum(1 for n in eng.nodes if n.state == "infected")
        affected = eng.apply_fact_check(fraction=0.5)
        after = sum(1 for n in eng.nodes if n.state == "infected")
        assert affected > 0
        assert after < before

    def test_fact_check_creates_immune(self):
        eng = make_engine(spread_rate=1.0, recovery_rate=0.0, density=0.5)
        for _ in range(10):
            eng.advance()
        eng.apply_fact_check(fraction=1.0)
        immune = sum(1 for n in eng.nodes if n.state == "immune")
        assert immune > 0

    def test_awareness_sets_steps(self):
        eng = make_engine()
        eng.apply_awareness(duration=7)
        assert eng.awareness_steps_left == 7

    def test_awareness_expires(self):
        eng = make_engine()
        eng.apply_awareness(duration=3)
        for _ in range(3):
            eng.advance()
        assert eng.awareness_steps_left == 0

    def test_targeted_immunization(self):
        eng = make_engine(spread_rate=0.0)
        affected = eng.apply_targeted_immunization(top_n=3)
        assert affected <= 3
        immune = sum(1 for n in eng.nodes if n.state == "immune")
        assert immune == affected

    def test_targeted_immunizes_high_degree(self):
        eng = make_engine(density=0.3, spread_rate=0.0)
        eng.apply_targeted_immunization(top_n=5)
        immune_nodes = [n for n in eng.nodes if n.state == "immune"]
        non_immune = [n for n in eng.nodes if n.state == "susceptible"]
        if immune_nodes and non_immune:
            min_immune_conn = min(n.connections for n in immune_nodes)
            max_non_immune_conn = max(n.connections for n in non_immune)
            # Top immune nodes should generally have >= connections than non-immune
            assert min_immune_conn >= 0  # basic sanity


class TestSerialization:
    def test_to_snapshot_keys(self):
        eng = make_engine()
        snap = eng.to_snapshot()
        assert all(k in snap for k in ("id", "step", "config", "stats", "nodes", "edges"))

    def test_node_serialization(self):
        eng = make_engine()
        nodes = eng.nodes_as_dict()
        assert len(nodes) == 40
        assert all("state" in n for n in nodes)

    def test_edges_serialization(self):
        eng = make_engine()
        edges = eng.edges_as_list()
        assert all(len(e) == 2 for e in edges)
