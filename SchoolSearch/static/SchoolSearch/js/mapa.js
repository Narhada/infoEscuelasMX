const map = L.map('map').setView([19.7008, -101.1844], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

L.marker([19.7008, -101.1844])
    .addTo(map)
    .bindPopup("Mapa funcionando")
    .openPopup();


