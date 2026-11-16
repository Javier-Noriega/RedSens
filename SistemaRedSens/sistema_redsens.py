from M1_hash.tabla_hash import Tablahash

from M2_arboles.abb import ABB
from M2_arboles.avl import AVL

from M6_simulacion.generador_estaciones import (
    GeneradorEstaciones
)


class SistemaRedSens:

    def __init__(self):

        self.tabla_hash = Tablahash(
            23,
            Tablahash.SONDEO_CUADRATICA
        )

        self.abb = ABB()

        self.avl = AVL()

        self.generador = (
            GeneradorEstaciones(
                5026
            )
        )