
from typing import Dict, List

REGIONS_CLIMATS = {
    "tropical": "Chaud et humide toute l’année",
    "subtropical": "Chaud, hiver doux, pluies saisonnières",
    "tempéré": "Saisons distinctes, été chaud, hiver froid",
    "méditerranéen": "Été chaud et sec, hiver doux et humide",
    "froid": "Zone froide au nord"
}


def definir_geolocalisation(lat: float = 40.8214, lon: float = 14.4265) -> Dict[str, float] :
    """
    Définir la position de la plantation.
    Par défaut : le Vésuve (Italie), idéeal pour planter les tomates!
    lat : latitude
    lon : longitude
    """
    
    abs_lat = abs(lat)
    # Définition symétrique des climats
    if 0 <= abs_lat <= 23:
        climat = "tropical"
    elif 23 < abs_lat <= 35:
        climat = "subtropical"
    elif 35 < abs_lat <= 50:
        climat = "méditerranéen"
    elif 50 < abs_lat <= 66:
        climat = "tempéré"
    else:
        climat = "froid"
    
    return {
        "lat": lat,
        "lon": lon,
        "climat": climat
    }