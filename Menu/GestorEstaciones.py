from Modelos.estacion import estacion

class GestorEstaciones:

    def __init__(self, sistema):
        self.sistema = sistema

    def registrar_estacion(self):
        codigo=input("Codigo: ")
        numero=input("Numero: ")
        nombreestacion=input("Nombre de la Estacion: ")
        localidad=input("Localidad: ")
        tipoestacion=input("Tipo de estacion: ")
        bateria=input("Bateria: ")
        diasSinVisita=input("Dias sin visita: ")
        nuevaEstacion=estacion(codigo,numero,nombreestacion,localidad,tipoestacion,bateria,diasSinVisita)
        self.sistema.tabla_hash.insertar(nuevaEstacion)
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

        eliminado = self.sistema.tabla_hash.eliminar(codigo)

        if eliminado:
            print("Estacion eliminada correctamente")
        else:
            print("Estacion no encontrada") 

    def mostrar_tabla(self):
        self.sistema.tabla_hash.mostrar()

    def mostrar_estadisticas(self):
        self.sistema.tabla_hash.mostrar_estadisticas()