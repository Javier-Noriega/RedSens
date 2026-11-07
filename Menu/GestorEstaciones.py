from Modelos.estacion import estacion
from config.localidades import LOCALIDADES

class GestorEstaciones:

    def __init__(self, sistema):
        self.sistema = sistema

    def registrar_estacion(self):

        codigo = input("Codigo: ")

        numero = int(input("Numero: "))

        nombreestacion = input("Nombre de la Estacion: ")

        print("\nLocalidades disponibles:\n")

        for i, localidad in enumerate(LOCALIDADES, start=1):
            print(f"{i}. {localidad}")

        opcion_localidad = int(
            input("\nSeleccione localidad: ")
        )

        if opcion_localidad < 1 or opcion_localidad > len(LOCALIDADES):
            print("Localidad invalida")
            return

        localidad = LOCALIDADES[
            opcion_localidad - 1
        ]

        tipoestacion = input("Tipo de estacion: ")

        bateria = int(input("Bateria: "))

        diasSinVisita = int(
            input("Dias sin visita: ")
        )

        nuevaEstacion=estacion(codigo,numero,nombreestacion,localidad,tipoestacion,bateria,diasSinVisita)

        self.sistema.tabla_hash.insertar(nuevaEstacion)
        self.sistema.abb.insertar(nuevaEstacion)
        self.sistema.avl.insertar(nuevaEstacion)
        
        print("\nEstacion registrada correctamente")

    def buscar_estacion(self):
        codigo = input("Codigo: ")

        estacion_encontrada = self.sistema.tabla_hash.buscar(codigo)

        if estacion_encontrada is None:
            print("Estacion no encontrada")
        else:
            print("\nEstacion encontrada:")
            print(f"Codigo: {estacion_encontrada.codigo}")
            print(f"Numero: {estacion_encontrada.numero}")
            print(f"Nombre: {estacion_encontrada.nombre}")
            print(f"Localidad: {estacion_encontrada.localidad}")
            print(f"Tipo: {estacion_encontrada.tipo}")
            print(f"Bateria: {estacion_encontrada.bateria}")
            print(f"Dias sin visita: {estacion_encontrada.diasSinVisita}")

    def eliminar_estacion(self):
        codigo = input("Codigo: ")
        estacion=self.sistema.tabla_hash.buscar(codigo)

        eliminado = self.sistema.tabla_hash.eliminar(codigo)
        self.sistema.abb.eliminar(estacion.numero)
        self.sistema.avl.eliminar(estacion.numero)

        if eliminado:
            print("Estacion eliminada correctamente")
        else:
            print("Estacion no encontrada") 

    def mostrar_tabla(self):
        self.sistema.tabla_hash.mostrar()

    def mostrar_estadisticas(self):
        self.sistema.tabla_hash.mostrar_estadisticas()