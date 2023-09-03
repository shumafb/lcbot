from bs4 import BeautifulSoup

bsinfos = [{'operator': 2, 'coord': '44.615500-40.078101', 'radius': '500'},
           {'operator': 25, 'coord': '44.618500-40.079101', 'radius': '500'},
           ]

operators = {1: 'red', 2: 'green', 25: 'black', 99: 'yellow'}
# for bsinfo in bsinfos:
#     print(bsinfo['operator'])
#     print(type(bsinfo['operator']))
#     print(bsinfo['coord'].split('-')[0])
#     print(bsinfo['coord'].split('-')[1])
#     print(bsinfo['radius'])



def constructor(bslist):
    with open('test.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    coords = []
    markers = []
    circles = []
    count = 0

    element = soup.find(id='locatorbs')

    # Координаты
    for bs in bslist:
        coords.append(f"    var coords{count} = [{bs['coord'].split('-')[0]}, {bs['coord'].split('-')[1]}];")
        count += 1

    # Маркеры с координатами
    count = 0
    for bs in bslist:
        markers.append(f"    L.marker(coords{count}).bindPopup({bs['coord'].split('-')[0]}, {bs['coord'].split('-')[1]}).addTo(map);")
        count += 1

    # Добавление кругов
    count = 0 
    for bs in bslist:

        circles.append(f"    L.circle(coords{count}, {{color: '{operators[bs['operator']]}', fillcolor: '{operators[bs['operator']]}', fillOpacity: 0.5, radius: {bs['radius']}}}).addTo(map);")
        count += 1

    coords = '\n'.join(coords)
    markers = '\n'.join(markers)
    circles = '\n'.join(circles)

    new_element = element.string+coords+'\n\n'+markers+'\n\n'+circles

    element.string = new_element


    # Запись в файл
    with open('test2.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))


constructor(bslist=bsinfos)