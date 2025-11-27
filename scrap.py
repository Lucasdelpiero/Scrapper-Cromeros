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

urls = ["https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=734",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=735",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=736",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=737",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=738",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=740",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=741",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=742",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=743",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=744",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=745",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=746",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=747",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=748",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=749",
        "https://dragonball.center/?load=dbc&catalogo&coleccion=500_dragon-ball-z-juego-de-cartas-coleccionables&grupo=750"
]
cont = 10
for url in urls:
    cont = cont + 1
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

    # Crear carpetas si no existen
    os.makedirs("iconos/" + str(cont), exist_ok=True)
    os.makedirs("imagenes/" + str(cont), exist_ok=True)

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
            with open("imagenes/" + os.path.join(str(cont) , nombre), "wb") as f:
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
            with open("iconos/" + os.path.join(str(cont), nombre), "wb") as f:
                f.write(response.content)

            print(f"✔ Guardado: {filename}")
        else:
            print(f"✖ Error descargando {card.icon}")




