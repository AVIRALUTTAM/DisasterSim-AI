async function predict() {
  let rainfall = document.getElementById("rainfall").value;
  let population = document.getElementById("population").value;
  let infra = document.getElementById("infra").value;

  let response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      rainfall: rainfall,
      population: population,
      infra: infra
    })
  });

  let data = await response.json();

  document.getElementById("result").innerHTML = `
    Severity: ${data.severity} <br>
    Risk: ${data.risk} <br>
    🚑 Ambulance: ${data.resources.ambulance} <br>
    👷 Teams: ${data.resources.teams} <br>
    🍱 Food: ${data.resources.food} <br>
    Action: ${data.action}
  `;
}
