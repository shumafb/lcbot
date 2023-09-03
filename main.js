        
    // Инициализация карты
    var map = L.map('map').setView([44.5654605, 40.076777], 13);

    // Добавление слоя тайлов
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Координаты
    var coords1 = [44.615500, 40.078101];
    var coords2 = [44.620000, 40.079201];
    var coords3 = [44.630000, 40.078301];
    var coords4 = [44.640000, 40.078401];

    // Добавление маркеров с координатами
    L.marker(coords1).bindPopup(coords1[0] + ', ' + coords1[1]).addTo(map);
    L.marker(coords2).bindPopup(coords2[0] + ', ' + coords2[1]).addTo(map);
    L.marker(coords3).bindPopup(coords3[0] + ', ' + coords3[1]).addTo(map);
    L.marker(coords4).bindPopup(coords4[0] + ', ' + coords4[1]).addTo(map);

    // Добавление кругов
    L.circle(coords1, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(map);

    L.circle(coords2, {
        color: 'green',
        fillColor: '#0f3',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(map);

    L.circle(coords3, {
        color: 'yellow',
        fillColor: '#ff0',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(map);

    L.circle(coords4, {
        color: 'black',
        fillColor: '#000',
        fillOpacity: 0.5,
        radius: 500
    }).addTo(map);


