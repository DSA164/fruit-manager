from fruit_manager import ouvrir_inventaire
from geolocalisation import definir_geolocalisation
from fruit import lire_fruits, creer_fruits
import random
import os
import json
import datetime
from typing import Dict, Any

PLANTATIONS_PATH = "data/plantations.json"
SUPERFICIE_PLANTATION_MIN = 500    #en m^2
SUPERFICIE_PLANTATION_MAX = 25000    #en m^2

def creer_plantation(lat: float = 40.8214, lon: float = 14.4265) -> Dict[str, Any]:
    """
    Crée une plantation avec géolocalisation, climat, répartition aléatoire des fruits
    et sauvegarde automatiquement dans le fichier JSON.

    Args:
        lat (float): Latitude de la plantation (ex: 40.8214)
        lon (float): Longitude de la plantation (ex: 14.4265)

    Returns:
        Dict[str, Any]: Dictionnaire représentant la plantation créée, comprenant :
            - 'geoloc': dict avec 'lat', 'lon' et 'climat'
            - 'climat': climat déterminé automatiquement à partir de la géolocalisation
            - 'superficie_totale': superficie totale de la plantation (float)
            - 'fruits_plantés': dictionnaire des fruits choisis et leur superficie
            - 'date_creation': date et heure de création (ISO string)
    """
    geoloc = definir_geolocalisation(lat=lat, lon=lon)
    climat = geoloc["climat"]

    liste_fruits = lire_fruits()

    fruits_compatibles = [
        fruit for fruit in liste_fruits if climat in fruit.get("regions", [])
    ]

    
    superficie_totale = round(random.uniform(SUPERFICIE_PLANTATION_MIN, SUPERFICIE_PLANTATION_MAX), 2)
    
    k = random.randint(1, len(fruits_compatibles))
    varietes_selectionnes = random.sample(fruits_compatibles, k=k)

    proportions = [random.random() for _ in range(k)]
    total_proportion = sum(proportions)
    repartition_superficie = {
        fruit["nom"]: int(superficie_totale * (p / total_proportion))
        for fruit, p in zip(varietes_selectionnes, proportions)
    }

    fruits_plantes = {
        fruit["nom"]: {
            "superficie [m\u00B2]": repartition_superficie[fruit["nom"]],
        }
        for fruit in varietes_selectionnes
    }

    plantation = {
        "geoloc": geoloc,
        "climat": climat,
        "superficie_totale [m\u00B2]": superficie_totale,
        "fruits_plantés": fruits_plantes,
        "date_creation": datetime.datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(PLANTATIONS_PATH), exist_ok=True)
    plantations_existantes = []
    if os.path.exists(PLANTATIONS_PATH):
        with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
            try:
                plantations_existantes = json.load(f)
            except:
                plantations_existantes = []

    plantations_existantes.append(plantation)

    with open(PLANTATIONS_PATH, "w", encoding="utf-8") as fichier:
        json.dump(plantations_existantes, fichier, ensure_ascii=False, indent=4)

    return plantation



def lire_plantations():
    """
    Lit toutes les plantations sauvegardées dans le fichier JSON.
    
    Returns:
        List[Dict[str, Any]]: Liste des plantations existantes. Chaque plantation
        est un dictionnaire structuré comme suit :
            - 'geoloc': dict avec
                - 'lat': latitude (float)
                - 'lon': longitude (float)
                - 'climat': climat déterminé automatiquement (str)
            - 'climat': climat de la plantation (str)
            - 'superficie_totale': superficie totale de la plantation en m² (float)
            - 'fruits_plantés': dictionnaire des fruits choisis, où chaque clé est
              le nom du fruit et la valeur un dictionnaire contenant :
                - 'superficie': superficie occupée par ce fruit (float)
                - 'specs': dictionnaire complet du fruit avec ses caractéristiques
            - 'date_creation': date et heure de création de la plantation (ISO string)
    """
    if os.path.exists(PLANTATIONS_PATH):
        with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


if __name__ == "__main__":
    creer_fruits()
    plantation_test = creer_plantation() 
    for key, value in plantation_test.items():
        print(key)
        print("-"*len(key))
        print(value, "\n")