import re
from colorama import Fore
import requests
from bs4 import BeautifulSoup
import json

# website
# https://www.mundodeportivo.com/resultados/futbol/premier-league/equipos


website = "https://www.mundodeportivo.com/resultados/futbol/premier-league/equipo/liverpool/plantilla"
# website = "https://www.mundodeportivo.com/resultados/futbol/copa-libertadores/equipo/nacional/plantilla"
# website = "https://www.mundodeportivo.com/resultados/futbol/premier-league/equipo/manchester-city/plantilla"
result = requests.get(website)
content = result.text

txt = "<div class=\"data__content\"><h2 class=\"data__title\">"
patron = r"{}([\w\s-]+)".format(re.escape(txt))

patron = r"data__title\">([\w\s-]+)"
players = re.findall(patron,str(content))

soup = BeautifulSoup(str(content), 'html.parser')
panel_groups = soup.find_all(class_="panel-group")

team= []
id_player = 1
for panel_group in panel_groups:

    table_header_tag = panel_group.find_previous_sibling(class_="table-header")
    if table_header_tag:
        posicion = table_header_tag.find('h2').get_text()
    else:
        print("No table header found")

    panel_bodies = panel_group.find_all(class_="panel__body")
    for panel_body in panel_bodies:
        data_side = panel_body.find(class_="data__side").find('img')['src']
        data_number = panel_body.find(class_="data__side").find(class_="data__number").get_text().strip()

        data_title = panel_body.find(class_="data__content").find(class_="data__title").get_text()

        number=data_number
        name=data_title
        height=""
        weight =""
        date_of_birth =""
        place_of_birth =""

        data_items = panel_body.find_all(class_="data-item")
        for item in data_items:
            item_title = item.find(class_="data-item__title").get_text()
            item_value = item.find(class_="data-item__value").get_text()

            if item_title.strip() == "Altura":
                height=item_value
            if item_title.strip() == "Peso":
                weight=item_value
            if item_title.strip() == "Fecha nacimiento":
                date_of_birth=item_value
            if item_title.strip() == "Lugar nacimiento":
                place_of_birth=item_value

        player={
            "Name":name,
            "Number":number,
            "Position":posicion,
            "Height":height,
            "Weight":weight,
            "DateOfBirth":date_of_birth,
            "PlaceOfBirth":place_of_birth,
            }
        team.append(player)

team_match = re.search(r"equipo/([^/]+)", website)
team_name = "team"
if team_match:
    team_name = team_match.group(1)
file_name = f'{team_name}.json'

# Convert the list of dictionaries to JSON and save it to a file
with open(file_name, 'w',encoding='utf-8') as f:
    json.dump(team, f, ensure_ascii=False)

print(f"File JSON '{file_name}' successfully created.")