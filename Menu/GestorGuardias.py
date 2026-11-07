from josephus.m5_josephus import (
    mostrar_calendario,
    comparar_rendimiento
)


class GestorGuardias:

    def __init__(self, sistema):
        self.sistema = sistema

    def generar_calendario(self):

        try:
            grupo = int(
                input(
                    "Numero de grupo (1-15): "
                )
            )

        except ValueError:

            print(
                "Debe ingresar un numero."
            )

            return

        if grupo < 1 or grupo > 15:

            print(
                "El numero de grupo "
                "debe estar entre 1 y 15."
            )

            return

        mostrar_calendario(grupo)

    def analizar_rendimiento(self):

        try:

            grupo = int(
                input(
                    "Numero de grupo (1-15): "
                )
            )

        except ValueError:

            print(
                "Debe ingresar un numero."
            )

            return

        if grupo < 1 or grupo > 15:

            print(
                "El numero de grupo "
                "debe estar entre 1 y 15."
            )

            return

        m_grupo = (
            (grupo - 1) % 4
        ) + 1

        comparar_rendimiento(
            m_grupo
        )