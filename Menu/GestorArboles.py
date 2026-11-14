from M2_arboles import prueba_m2


class GestorArboles:

    def __init__(self, sistema):
        self.sistema = sistema

    def buscar_por_numero(self):

        try:
            numero = int(input("Numero de estacion: "))
        except ValueError:
            print("Debe ingresar un numero.")
            return

        estacion = self.sistema.avl.buscar(numero)

        if estacion is None:
            print("Estacion no encontrada.")
            return

        self._mostrar_estacion(estacion)

    def buscar_por_rango(self):

        try:
            desde = int(input("Desde: "))
            hasta = int(input("Hasta: "))
        except ValueError:
            print("Debe ingresar numeros.")
            return

        estaciones = self.sistema.avl.rango(desde, hasta)

        if not estaciones:
            print("No se encontraron estaciones.")
            return

        for estacion in estaciones:
            self._mostrar_estacion(estacion)

    def mostrar_estaciones_criticas(self):

        criticas = self.sistema.avl.criticas()

        if not criticas:
            print("No hay estaciones criticas.")
            return

        print("\n=== ESTACIONES CRITICAS ===")

        for estacion in criticas:
            self._mostrar_estacion(estacion)

    def mostrar_estadisticas(self):

        print("\n=== ESTADISTICAS AVL ===")
        print("Altura :", self.sistema.avl.altura())
        print("Nodos  :", self.sistema.avl.cantidad_nodos())
        print("Hojas  :", self.sistema.avl.cantidad_hojas())

    def ejecutar_experimento(self):

        prueba_m2.experimento()

    def _mostrar_estacion(self, estacion):

        print(
            f"{estacion.codigo} | "
            f"{estacion.numero} | "
            f"{estacion.nombre} | "
            f"{estacion.localidad} | "
            f"Bateria: {estacion.bateria}%"
        )