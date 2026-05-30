"""
Algoritmo de asignación inteligente de rutas para buses.
Utiliza Dijkstra y criterios de demanda para asignar rutas óptimas.
"""

import random
from database import SessionLocal
from models import VehiculoDB, RutaDB, ParadaDB
from graph_engine import GrafoMetropolitano


class AsignadorRutasInteligente:
    """
    Asigna rutas a buses de forma inteligente basada en:
    - Demanda de pasajeros (demanda_promedio)
    - Capacidad del bus
    - Eficiencia energética (Eléctrico vs Gasolina)
    - Distancia óptima (Dijkstra)
    """

    def __init__(self):
        self.db = SessionLocal()
        self.grafo = GrafoMetropolitano()

    def obtener_ruta_optima_por_demanda(self) -> RutaDB:
        """
        Selecciona la ruta con mayor demanda promedio.
        Las rutas con más pasajeros potenciales son prioritarias.
        """
        rutas = self.db.query(RutaDB).all()
        
        if not rutas:
            return None
        
        # Ordenar por demanda_promedio descendente
        ruta_optima = max(rutas, key=lambda r: r.demanda_promedio)
        
        return ruta_optima

    def obtener_ruta_optima_por_distancia(self) -> RutaDB:
        """
        Selecciona la ruta más corta.
        Útil para buses con baja energía o urgencia de tiempo.
        """
        rutas = self.db.query(RutaDB).all()
        
        if not rutas:
            return None
        
        # Ordenar por distancia_km ascendente
        ruta_optima = min(rutas, key=lambda r: r.distancia_km)
        
        return ruta_optima

    def obtener_ruta_optima_por_eficiencia(self, tipo_motor: str) -> RutaDB:
        """
        Selecciona ruta considerando eficiencia energética.
        - Buses eléctricos: prefieren rutas cortas (menos carga)
        - Buses gasolina: pueden hacer rutas largas
        """
        rutas = self.db.query(RutaDB).all()
        
        if not rutas:
            return None
        
        if tipo_motor == "Electrico":
            # Preferir rutas cortas para evitar descarga
            ruta_optima = min(rutas, key=lambda r: r.distancia_km)
        else:
            # Buses gasolina pueden hacer rutas más demandantes
            ruta_optima = max(rutas, key=lambda r: r.demanda_promedio)
        
        return ruta_optima

    def asignar_ruta_a_bus(self, vehiculo_id: int) -> RutaDB:
        """
        Algoritmo de asignación inteligente.
        Considera: capacidad, tipo motor, demanda actual.
        """
        vehiculo = self.db.query(VehiculoDB).filter_by(id=vehiculo_id).first()
        
        if not vehiculo:
            return None

        # Obtener todas las rutas
        rutas = self.db.query(RutaDB).all()
        
        if not rutas:
            return None

        # CRITERIO 1: Capacidad del bus
        # Buses grandes (60-80) -> rutas con alta demanda
        # Buses pequeños (40) -> rutas con baja demanda
        
        rutas_filtradas = []
        
        if vehiculo.capacidad >= 60:
            # Buses grandes: prefieren rutas con alta demanda
            rutas_filtradas = sorted(
                rutas,
                key=lambda r: r.demanda_promedio,
                reverse=True
            )[:5]  # Top 5 rutas con mayor demanda
        
        elif vehiculo.capacidad == 40:
            # Buses pequeños: rutas equilibradas
            rutas_filtradas = sorted(
                rutas,
                key=lambda r: r.distancia_km
            )[:5]  # Top 5 rutas más cortas
        
        # CRITERIO 2: Tipo de motor
        # Eléctricos prefieren rutas cortas
        # Gasolina pueden hacer rutas más largas
        
        if vehiculo.tipo_motor == "Electrico":
            ruta_asignada = min(
                rutas_filtradas,
                key=lambda r: r.distancia_km
            )
        else:
            # Gasolina: preferir demanda si está disponible
            ruta_asignada = max(
                rutas_filtradas,
                key=lambda r: r.demanda_promedio
            )

        return ruta_asignada

    def asignar_todas_las_rutas(self):
        """
        Asigna rutas a todos los buses del sistema.
        Registra las asignaciones en la BD.
        """
        vehiculos = self.db.query(VehiculoDB).all()
        asignaciones = []

        for vehiculo in vehiculos:
            ruta = self.asignar_ruta_a_bus(vehiculo.id)
            
            if ruta:
                vehiculo.ruta_asignada_id = ruta.id
                vehiculo.estado_operacion = "EN_SERVICIO"
                asignaciones.append({
                    "vehiculo_id": vehiculo.id,
                    "placa": vehiculo.placa,
                    "ruta_id": ruta.id,
                    "ruta_nombre": ruta.nombre,
                    "distancia_km": ruta.distancia_km,
                    "demanda": ruta.demanda_promedio
                })

        self.db.commit()
        
        return asignaciones

    def obtener_asignaciones_actuales(self) -> list:
        """
        Retorna todas las asignaciones actuales de buses.
        """
        vehiculos = self.db.query(VehiculoDB).filter(
            VehiculoDB.ruta_asignada_id.isnot(None)
        ).all()

        asignaciones = []
        
        for v in vehiculos:
            ruta = self.db.query(RutaDB).filter_by(id=v.ruta_asignada_id).first()
            
            if ruta:
                asignaciones.append({
                    "vehiculo_id": v.id,
                    "placa": v.placa,
                    "tipo_motor": v.tipo_motor,
                    "capacidad": v.capacidad,
                    "ruta_id": ruta.id,
                    "ruta_nombre": ruta.nombre,
                    "ruta_codigo": ruta.codigo_ruta,
                    "distancia_km": ruta.distancia_km,
                    "tiempo_min": ruta.tiempo_estimado_min,
                    "demanda": ruta.demanda_promedio
                })

        return asignaciones

    def reasignar_por_congestión(self, vehiculo_id: int, congestión_actual: float):
        """
        Si una ruta está congestionada (>80%), reasignar a otra.
        """
        if congestión_actual > 0.8:
            ruta_alternativa = self.asignar_ruta_a_bus(vehiculo_id)
            
            vehiculo = self.db.query(VehiculoDB).filter_by(id=vehiculo_id).first()
            
            if vehiculo and ruta_alternativa:
                vehiculo.ruta_asignada_id = ruta_alternativa.id
                self.db.commit()
                
                return ruta_alternativa
        
        return None

    def estadisticas_asignacion(self) -> dict:
        """
        Retorna estadísticas sobre la asignación de rutas.
        """
        vehiculos = self.db.query(VehiculoDB).all()
        rutas = self.db.query(RutaDB).all()

        asignados = len([v for v in vehiculos if v.ruta_asignada_id])
        sin_asignar = len(vehiculos) - asignados

        distribución_rutas = {}
        for ruta in rutas:
            count = len([v for v in vehiculos if v.ruta_asignada_id == ruta.id])
            if count > 0:
                distribución_rutas[ruta.nombre] = count

        return {
            "total_buses": len(vehiculos),
            "buses_asignados": asignados,
            "buses_sin_asignar": sin_asignar,
            "total_rutas": len(rutas),
            "distribucion_por_ruta": distribución_rutas,
            "promedio_buses_por_ruta": round(asignados / len(rutas) if rutas else 0, 1)
        }
