from M6_simulacion.generador_estaciones import (
    GeneradorEstaciones
)

from M6_simulacion.validacion_semillas import (
    secuencias_iguales,
    secuencias_distintas
)

from M6_simulacion.uniformidad import (
    comprobar_uniformidad
)

from M6_simulacion.experimento_m1 import (
    ejecutar as experimento_m1
)

from M6_simulacion.experimento_m2 import (
    ejecutar as experimento_m2
)

from M6_simulacion.experimento_m5 import (
    ejecutar as experimento_m5
)

from M6_simulacion.rendimiento import (
    ejecutar_todos
)


class GestorSimulacion:

    def __init__(self, sistema):
        self.sistema = sistema

    def generar_estaciones(self):

        try:
            cantidad = int(
                input(
                    "Cantidad de estaciones: "
                )
            )

        except ValueError:

            print(
                "Debe ingresar un numero."
            )

            return

        generador = GeneradorEstaciones(
            5026
        )

        estaciones = (
            generador.generar_estaciones(
                cantidad
            )
        )

        for e in estaciones:

            self.sistema.tabla_hash.insertar(e)

            self.sistema.abb.insertar(e)

            self.sistema.avl.insertar(e)

        print(
            f"{cantidad} estaciones cargadas."
        )

    def validar_semillas(self):

        print(
            "\nMisma semilla:",
            secuencias_iguales()
        )

        print(
            "Distinta semilla:",
            secuencias_distintas()
        )

    def uniformidad(self):

        resultado = comprobar_uniformidad()

        print(
            "\nUNIFORMIDAD"
        )

        for rango, cantidad in resultado.items():

            print(
                f"{rango} -> {cantidad}"
            )

    def experimento_m1(self):
        experimento_m1()

    def experimento_m2(self):
        experimento_m2()

    def experimento_m5(self):
        experimento_m5()

    def bateria_completa(self):
        ejecutar_todos()