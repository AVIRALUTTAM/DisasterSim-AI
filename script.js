let chart;

function predict() {
  let rainfall = parseFloat(document.getElementById("rainfall").value);
  let population = parseFloat(document.getElementById("population").value);
  let infra = document.getElementById("infra").value;

  if (!rainfall || !population) {
    alert("Please enter all values!");
    return;
  }

  // Severity Calculation
  let infraWeight = {
    "Low": 1.5,
    "Medium": 1.0,
    "High": 0.6
  };

  let score = (rainfall * 0.6 + population * 0.4) * infraWeight[infra];

  let level, color, suggestion;

  if (score < 50) {
    level = "Low 🟢";
    color = "green";
    suggestion = "Monitor situation";
  } else if (score < 100) {
    level = "Medium 🟡";
    color = "yellow";
    suggestion = "Prepare rescue teams";
  } else {
    level = "High 🔴";
    color = "red";
    suggestion = "Emergency evacuation required";
  }

  // Show result
  document.getElementById("result").innerHTML =
    `<b>Severity:</b> ${score.toFixed(2)} <br>
     <b>Risk:</b> <span style="color:${color}">${level}</span><br>
     <b>Action:</b> ${suggestion}`;

  // Resource Allocation
  let resources = getResources(score);
  document.getElementById("result").innerHTML += `
    <br><b>Resources:</b><br>
    🚑 Ambulances: ${resources.ambulance}<br>
    👷 Teams: ${resources.teams}<br>
    🍱 Food Packs: ${resources.food}
  `;

  // Chart
  showChart(score);
}

function getResources(score) {
  if (score < 50) {
    return { ambulance: 2, teams: 1, food: 50 };
  } else if (score < 100) {
    return { ambulance: 5, teams: 3, food: 150 };
  } else {
    return { ambulance: 10, teams: 6, food: 300 };
  }
}

function showChart(score) {
  let ctx = document.getElementById("chart").getContext("2d");

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Severity"],
      datasets: [{
        label: "Impact Level",
        data: [score]
      }]
    }
  });
}
