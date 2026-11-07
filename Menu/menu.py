from Menu.GestorEstaciones import GestorEstaciones
from Menu.GestorArboles import GestorArboles
from Menu.GestorGrafos import GestorGrafos
from Menu.GestorCompresion import GestorCompresion
from Menu.GestorGuardias import GestorGuardias

class Menu:

    def __init__(self, sistema):

        self.sistema = sistema
        self.gestor_estaciones = GestorEstaciones(sistema)
        self.gestor_arboles = GestorArboles(sistema)
        self.gestor_grafos = GestorGrafos(sistema)
        self.gestor_compresion = GestorCompresion(sistema)
        self.gestor_guardias = GestorGuardias(sistema)

    def mostrar(self):

        while True:

            print("\n====================================")
            print(" REDSENS")
            print("====================================")
            print("1. Gestion de estaciones")
            print("2. Consultas Avanzadas")
            print("3. Red vial")
            print("4. Compresión de mediciones")
            print("5. Gestion de guardias")
            print("0. Salir")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                self.menu_estaciones()

            elif opcion== "2":
                self.menu_arboles()

            elif opcion== "3":
                self.menu_grafos()

            elif opcion == "4":
                self.menu_compresion()

            elif opcion == "5":
                self.menu_guardias()

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

    def menu_arboles(self):

        while True:

            print("\n====================================")
            print(" CONSULTAS AVANZADAS")
            print("====================================")
            print("1. Buscar estacion por numero")
            print("2. Buscar estaciones por rango")
            print("3. Ver estaciones criticas")
            print("4. Ver estadisticas AVL")
            print("5. Ejecutar experimento ABB vs AVL")
            print("0. Volver")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                self.gestor_arboles.buscar_por_numero()

            elif opcion == "2":
                self.gestor_arboles.buscar_por_rango()

            elif opcion == "3":
                self.gestor_arboles.mostrar_estaciones_criticas()

            elif opcion == "4":
                self.gestor_arboles.mostrar_estadisticas()

            elif opcion == "5":
                self.gestor_arboles.ejecutar_experimento()

            elif opcion == "0":
                break

            else:
                print("Opcion invalida")

    def menu_grafos(self):

        while True:

            print("\n====================================")
            print(" RED VIAL")
            print("====================================")
            print("1. Ver localidades")
            print("2. Lista de adyacencia")
            print("3. Matriz de adyacencia")
            print("4. BFS")
            print("5. DFS")
            print("6. Dijkstra")
            print("7. Floyd")
            print("8. Planificar visitas")
            print("0. Volver")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                self.gestor_grafos.ver_localidades()

            elif opcion == "2":
                self.gestor_grafos.ver_lista_adyacencia()

            elif opcion == "3":
                self.gestor_grafos.ver_matriz()

            elif opcion == "4":
                self.gestor_grafos.ejecutar_bfs()

            elif opcion == "5":
                self.gestor_grafos.ejecutar_dfs()

            elif opcion == "6":
                self.gestor_grafos.ejecutar_dijkstra()

            elif opcion == "7":
                self.gestor_grafos.ejecutar_floyd()

            elif opcion == "8":
                self.gestor_grafos.planificar_visitas()

            elif opcion == "0":
                break

            else:
                print("Opcion invalida")

    def menu_compresion(self):

        while True:

            print("\n====================================")
            print(" COMPRESION DE MEDICIONES")
            print("====================================")
            print("1. Verificar ejemplo Huffman")
            print("2. Generar archivo de mediciones")
            print("3. Comprimir archivo de mediciones")
            print("4. Ver metricas de compresion")
            print("5. Validar descompresion")
            print("6. Ver estado del proceso")
            print("0. Volver")

            opcion = input("\nOpcion: ")

            if opcion == "1":
                self.gestor_compresion.verificar_ejemplo_huffman()

            elif opcion == "2":
                self.gestor_compresion.generar_mediciones()

            elif opcion == "3":
                self.gestor_compresion.comprimir_archivo()

            elif opcion == "4":
                self.gestor_compresion.mostrar_metricas()

            elif opcion == "5":
                self.gestor_compresion.validar_descompresion()

            elif opcion == "6":
                self.gestor_compresion.mostrar_estado()

            elif opcion == "0":
                break

            else:
                print("Opcion invalida")

    def menu_guardias(self):

        while True:

            print("\n====================================")
            print(" GESTION DE GUARDIAS")
            print("====================================")
            print("1. Generar calendario")
            print("2. Analizar rendimiento")
            print("0. Volver")

            opcion = input("\nOpcion: ")

            if opcion == "1":

                self.gestor_guardias.generar_calendario()

            elif opcion == "2":

                self.gestor_guardias.analizar_rendimiento()

            elif opcion == "0":

                break

            else:

                print(
                    "Opcion invalida"
                )