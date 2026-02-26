from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== Severity Calculation =====
def calculate_severity(rainfall, population, infra):
    infra_weight = {
        "low": 1.5,
        "medium": 1.0,
        "high": 0.6
    }

    score = (rainfall * 0.6 + population * 0.4) * infra_weight[infra]
    return score

# ===== Resource Allocation =====
def get_resources(score):
    if score < 50:
        return {
            "risk": "Low",
            "ambulance": 2,
            "teams": 1,
            "food": 50,
            "action": "Monitor situation"
        }
    elif score < 100:
        return {
            "risk": "Medium",
            "ambulance": 5,
            "teams": 3,
            "food": 150,
            "action": "Prepare rescue teams"
        }
    else:
        return {
            "risk": "High",
            "ambulance": 10,
            "teams": 6,
            "food": 300,
            "action": "Emergency evacuation required"
        }

# ===== API ROUTE =====
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    rainfall = float(data["rainfall"])
    population = float(data["population"])
    infra = data["infra"].lower()

    score = calculate_severity(rainfall, population, infra)
    result = get_resources(score)

    return jsonify({
        "severity": round(score, 2),
        "risk": result["risk"],
        "resources": {
            "ambulance": result["ambulance"],
            "teams": result["teams"],
            "food": result["food"]
        },
        "action": result["action"]
    })

# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(debug=True)
