const map = L.map('map').setView([41.9, -87.9], 7);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let radarLayer;
let alertsLayer;
let spcLayer;

function loadRadar() {
  const product = document.getElementById("product").value;

  if (radarLayer) map.removeLayer(radarLayer);

  const url = `http://127.0.0.1:5000/radar?product=${product}&t=${Date.now()}`;

  radarLayer = L.imageOverlay(url, [[30, -100], [50, -80]]);
  radarLayer.addTo(map);
}

// Sweep animation (fake)
function sweepEffect() {
  const mapPane = document.querySelector('.leaflet-overlay-pane');
  mapPane.style.transition = "clip-path 1s linear";

  let angle = 0;
  setInterval(() => {
    angle = (angle + 20) % 360;
    mapPane.style.clipPath = `polygon(50% 50%, 100% 0%, 100% 100%)`;
  }, 100);
}

function toggleAlerts() {
  if (alertsLayer) {
    map.removeLayer(alertsLayer);
    alertsLayer = null;
    return;
  }

  fetch("http://127.0.0.1:5000/alerts")
    .then(res => res.json())
    .then(data => {
      alertsLayer = L.geoJSON(data, {
        style: f => ({ color: "red" })
      }).addTo(map);
    });
}

function toggleSPC() {
  if (spcLayer) {
    map.removeLayer(spcLayer);
    spcLayer = null;
    return;
  }

  fetch("http://127.0.0.1:5000/spc")
    .then(res => res.json())
    .then(data => {
      spcLayer = L.geoJSON(data, {
        style: f => ({ color: "orange" })
      }).addTo(map);
    });
}

document.getElementById("product").addEventListener("change", loadRadar);

loadRadar();
sweepEffect();
