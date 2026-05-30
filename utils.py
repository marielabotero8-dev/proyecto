import math
import json
from math import radians, sin, cos, sqrt, atan2

# ==========================================
# CÁLCULOS GEOGRÁFICOS
# ==========================================

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en KM entre dos puntos geográficos.
    
    Args:
        lat1, lon1: Latitud/Longitud punto 1
        lat2, lon2: Latitud/Longitud punto 2
    
    Returns:
        float: Distancia en kilómetros
    """
    R = 6371  # Radio de la Tierra en km
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def calcular_distancia_ruta(path):
    """
    Calcula la distancia total de una ruta (lista de coordenadas).
    
    Args:
        path: Lista de [lon, lat] o [[lon, lat], [lon, lat], ...]
    
    Returns:
        float: Distancia total en km
    """
    if not path or len(path) < 2:
        return 0.0
    
    distancia_total = 0.0
    
    for i in range(len(path) - 1):
        lon1, lat1 = path[i]
        lon2, lat2 = path[i + 1]
        distancia_total += haversine(lat1, lon1, lat2, lon2)
    
    return round(distancia_total, 2)


def calcular_tiempo_estimado(distancia_km, velocidad_promedio_kmh=30):
    """
    Calcula el tiempo estimado de una ruta.
    
    Args:
        distancia_km: Distancia en kilómetros
        velocidad_promedio_kmh: Velocidad promedio asumida (default 30 km/h para ciudad)
    
    Returns:
        float: Tiempo en minutos
    """
    if distancia_km == 0 or velocidad_promedio_kmh == 0:
        return 0.0
    
    horas = distancia_km / velocidad_promedio_kmh
    minutos = horas * 60
    
    return round(minutos, 1)


def calcular_demanda_promedio(paradas_personas):
    """
    Calcula la demanda promedio de una ruta basada en personas esperando en paradas.
    
    Args:
        paradas_personas: Lista de personas esperando en cada parada
    
    Returns:
        int: Promedio de personas por parada
    """
    if not paradas_personas:
        return 0
    
    return int(sum(paradas_personas) / len(paradas_personas))


# ==========================================
# CONVERSIONES
# ==========================================

def path_json_a_lista(path_json):
    """
    Convierte geometría_ruta JSON a lista de coordenadas.
    
    Args:
        path_json: String JSON con path
    
    Returns:
        list: Lista de [lon, lat]
    """
    try:
        return json.loads(path_json)
    except:
        return []


# ==========================================
# VALIDACIONES
# ==========================================

def validar_coordenadas(lat, lon):
    """Valida que las coordenadas sean válidas para Risaralda."""
    return (4.75 <= lat <= 5.40) and (-76.10 <= lon <= -75.50)
