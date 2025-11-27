from bs4 import BeautifulSoup
import requests
import os

IMAGEN = 'catalogo_coleccion_objeto_imagen'
INFO = 'catalogo_coleccion_objeto_info'

class Card(object):
    name = ""
    icon = ""
    image = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, icon, image):
        self.name = name
        self.icon = icon
        self.image = image

def make_card(name, icon, image):
    card = Card(name, icon, image)
    return card

url = "https://dragonball.center/catalogo/coleccion/1221/dragon-ball-z-juego-de-cartas-coleccionables"
result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")
objetos = doc.find_all("div", class_= "catalogo_coleccion_objeto")

#print(doc.prettify())
cards = []

# Crea cartas usando la data de la pagina
for obj in objetos:
    hijos = obj.find_all("div")     # o el nombre del tag que necesites
    nombre = ""
    icon = ""
    image = ""
    for hijo in hijos:
        if hijo:
            clase = hijo.get("class")[0]
            if clase == INFO:
                s = hijo.find("span")
                nombre = s.contents[0]
            
            elif clase == IMAGEN:
                style = hijo.get("style", "")
                # Extraer la URL dentro de url(...)
                start = style.find("url(")
                if start != -1:
                    start += 4
                    end = style.find(")", start)
                    urli = style[start:end].strip("'\"")
                icon = "https://dragonball.center" + urli

                image = hijo.get("onclick")
                image = "https://dragonball.center" + image.split("visor('")[1].split(",")[0].strip("'")
    cards.append(make_card(nombre, icon, image))             


for card in cards:
    print(card.name)
    print(card.icon)
    print(card.image)
    print()

# Crear carpetas si no existen
os.makedirs("iconos", exist_ok=True)
os.makedirs("imagenes", exist_ok=True)

# Descarga imagenes e iconos
for card in cards:
    # DESCARGA IMAGENES
    print(f"Descargando imagen {card.name}...")

    response = requests.get(card.image)

    if response.status_code == 200:
        # Guardar como nombre.jpg (o lo que corresponda)
        extension = card.image.split('.')[-1]
        filename = f"{card.name}.{extension}"

        nombre = f"{card.name}.jpg"
        with open(os.path.join("imagenes", nombre), "wb") as f:
            f.write(response.content)

        print(f"✔ Guardado: {filename}")
    else:
        print(f"✖ Error descargando {card.icon}")
    

    # DESCARGA ICONOS
    print(f"Descargando icono {card.name}...")

    response = requests.get(card.icon)

    if response.status_code == 200:
        # Guardar como nombre.jpg (o lo que corresponda)
        extension = card.icon.split('.')[-1]
        filename = f"{card.name}.{extension}"

        nombre = f"{card.name}.jpg"
        with open(os.path.join("iconos", nombre), "wb") as f:
            f.write(response.content)

        print(f"✔ Guardado: {filename}")
    else:
        print(f"✖ Error descargando {card.icon}")




