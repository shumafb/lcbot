from bs4 import BeautifulSoup

# bsinfos = [
#     {"operator": 2, "coord": "44.615500-40.078101", "radius": "500"},
#     {"operator": 25, "coord": "44.618500-40.079101", "radius": "500"},
# ]



def constructor(bslist, lclist):
    """Функция принимает список словарей с характеристиками базовых станций,
    возвращает тело html-страницы"""
    operators = {1: "red", 2: "green", 20: "black", 99: "yellow"}
    with open("/home/user/bot/lcbot/main.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    coords = []
    markers = []
    circles = []
    count = 0

    element = soup.find(id="locatorbs")

    main = f"\n    var map = L.map('map').setView([{bslist[0]['coord'].split('-')[0]}, {bslist[0]['coord'].split('-')[1]}], 13);"
    main += "\n    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {"
    main += "\n        attribution: '&copy; <a href=""http://www.openstreetmap.org/copyright"">OpenStreetMap</a>'"
    main += "\n    }).addTo(map);"
    # Координаты
    for bs in bslist:
        coords.append(
            f"    var coords{count} = [{bs['coord'].split('-')[0]}, {bs['coord'].split('-')[1]}];"
        )
        count += 1

    # Маркеры с координатами
    count = 0
    for bs in bslist:
        markers.append(
            # f"    L.marker(coords{count}).bindPopup(coords{count}[0] + ', ' + coords{count}[1]).addTo(map);"
            f"    L.marker(coords{count}).bindPopup('{lclist[count]}').addTo(map);"
        )
        count += 1

    # Добавление кругов
    count = 0
    for bs in bslist:
        operator_color = operators[int(bs['operator'])]
        circles.append(
            f"    L.circle(coords{count}, {{color: '{operator_color}', fillcolor: '{operator_color}', fillOpacity: 0.3, radius: 600}}).addTo(map);"
        )
        count += 1

    coords = "\n".join(coords)
    markers = "\n".join(markers)
    circles = "\n".join(circles)

    element.string = main + "\n\n" + coords + "\n\n" + markers + "\n\n" + circles

    # Запись в файл
    with open("/home/user/bot/lcbot/test2.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

