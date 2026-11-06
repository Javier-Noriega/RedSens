from Menu.GestorEstaciones import GestorEstaciones

class Menu:

    def __init__(self, sistema):
        self.sistema = sistema
        self.gestor_estaciones = GestorEstaciones(sistema)

    def mostrar(self):

        while True:

            print("\n====================================")
            print(" REDSENS")
            print("====================================")
            print("1. Gestion de estaciones")
            print("0. Salir")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                self.menu_estaciones()

            elif opcion == "0":
                print("Saliendo...")
                break

            else:
                print("Opcion invalida")

    def menu_estaciones(self):

            while True:

                print("\n====================================")
                print(" GESTION DE ESTACIONES")
                print("====================================")
                print("1. Registrar estacion")
                print("2. Buscar estacion")
                print("3. Eliminar estacion")
                print("4. Mostrar tabla")
                print("5. Estadisticas")
                print("0. Volver")

                opcion = input("\nOpcion: ")

                if opcion=="1":
                   self.gestor_estaciones.registrar_estacion()
                elif opcion == "2":
                    self.gestor_estaciones.buscar_estacion()

                elif opcion == "3":
                    self.gestor_estaciones.eliminar_estacion()

                elif opcion == "4":
                    self.gestor_estaciones.mostrar_tabla()

                elif opcion == "5":
                    self.gestor_estaciones.mostrar_estadisticas()

                elif opcion == "0":
                    break

                else:
                    print("Opcion invalida")