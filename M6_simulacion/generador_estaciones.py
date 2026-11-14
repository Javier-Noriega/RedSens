import random

from Modelos.estacion import estacion
from config.localidades import LOCALIDADES


class GeneradorEstaciones:

    TIPOS = [
        "PLUVIOMETRICA",
        "METEOROLOGICA",
        "HIDROMETRICA"
    ]

    def __init__(self, semilla):

        self.random = random.Random(
            semilla
        )

    def generar_estacion(
        self,
        numero
    ):

        codigo = f"CBA-{numero:04d}"

        return estacion(
            codigo,
            numero,
            f"Estacion {numero}",
            self.random.choice(
                LOCALIDADES
            ),
            self.random.choice(
                self.TIPOS
            ),
            self.random.randint(
                0,
                100
            ),
            self.random.randint(
                0,
                365
            )
        )

    def generar_estaciones(
        self,
        cantidad
    ):

        estaciones = []

        for numero in range(
            1,
            cantidad + 1
        ):

            estaciones.append(
                self.generar_estacion(
                    numero
                )
            )

        return estaciones