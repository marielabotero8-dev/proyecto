import numpy as np

from database import SessionLocal
from models import (
    ParadaDB,
    RutaParadaDB
)


class GrafoMetropolitano:

    def __init__(self):

        self.db = SessionLocal()

        self.paradas = (
            self.db.query(ParadaDB)
            .order_by(ParadaDB.id)
            .all()
        )

        self.nodos = {
            parada.id: idx
            for idx, parada in enumerate(self.paradas)
        }

        self.nombres = {
            parada.id: parada.nombre
            for parada in self.paradas
        }

        n = len(self.paradas)

        self.matriz_adyacencia = np.zeros(
            (n, n),
            dtype=int
        )

        self.construir_grafo()

    def construir_grafo(self):

        rutas = (
            self.db.query(RutaParadaDB)
            .order_by(
                RutaParadaDB.ruta_id,
                RutaParadaDB.orden_secuencia
            )
            .all()
        )

        rutas_dict = {}

        for r in rutas:

            rutas_dict.setdefault(
                r.ruta_id,
                []
            ).append(
                r.parada_id
            )

        for ruta_id, secuencia in rutas_dict.items():

            for i in range(
                len(secuencia) - 1
            ):

                origen = self.nodos[
                    secuencia[i]
                ]

                destino = self.nodos[
                    secuencia[i + 1]
                ]

                self.matriz_adyacencia[
                    origen,
                    destino
                ] = 1

                self.matriz_adyacencia[
                    destino,
                    origen
                ] = 1

    def obtener_matriz(self):

        return self.matriz_adyacencia.tolist()

    def grado_nodo(self, parada_id):

        idx = self.nodos[parada_id]

        return int(
            np.sum(
                self.matriz_adyacencia[idx]
            )
        )

    def centralidad(self):

        resultado = []

        for parada_id in self.nodos:

            resultado.append({
                "parada_id": parada_id,
                "nombre": self.nombres[parada_id],
                "grado": self.grado_nodo(
                    parada_id
                )
            })

        resultado.sort(
            key=lambda x: x["grado"],
            reverse=True
        )

        return resultado