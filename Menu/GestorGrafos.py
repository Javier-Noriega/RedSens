from grafos.grafo import (
    localidades,
    lista_adyacencia,
    matriz_adyacencia,
    bfs,
    dfs,
    dijkstra,
    floyd,
    reconstruir_camino,
    mostrar_matriz_distancias,
    plan_visitas
)


class GestorGrafos:

    def __init__(self, sistema):
        self.sistema = sistema

    def ver_localidades(self):

        print("\nLOCALIDADES")

        for localidad in localidades:
            print("-", localidad)

    def ver_lista_adyacencia(self):

        for i in range(len(localidades)):

            print(localidades[i], "->", end=" ")

            for vecino, km in lista_adyacencia[i]:

                print(
                    f"{localidades[vecino]} ({km} km)",
                    end=" ; "
                )

            print()

    def ver_matriz(self):

        mostrar_matriz_distancias(
            localidades,
            matriz_adyacencia,
            "Matriz de Adyacencia"
        )

    def ejecutar_bfs(self):

        origen = input("Localidad origen: ")

        if origen not in localidades:
            print("Localidad inexistente")
            return

        niveles = bfs(
            localidades,
            lista_adyacencia,
            origen
        )

        for i in range(len(localidades)):
            print(
                f"{localidades[i]} -> Nivel {niveles[i]}"
            )

    def ejecutar_dfs(self):

        recorrido = dfs(
            localidades,
            lista_adyacencia,
            "Deán Funes"
        )

        print("\nRecorrido DFS:")

        for indice in recorrido:
            print("-", localidades[indice])

    def ejecutar_dijkstra(self):

        distancias, predecesores = dijkstra(
            localidades,
            lista_adyacencia,
            "Deán Funes"
        )

        origen = localidades.index("Deán Funes")

        for destino in range(len(localidades)):

            camino = reconstruir_camino(
                localidades,
                origen,
                destino,
                predecesores
            )

            print(
                f"{localidades[destino]}"
                f" | {distancias[destino]} km"
                f" | {' -> '.join(camino)}"
            )

    def ejecutar_floyd(self):

        resultado = floyd(
            matriz_adyacencia
        )

        mostrar_matriz_distancias(
            localidades,
            resultado,
            "Distancias Minimas"
        )

    def planificar_visitas(self):

        criticas = self.sistema.avl.criticas()

        if not criticas:
            print("No hay estaciones criticas.")
            return

        localidades_criticas = []

        for estacion in criticas:

            if (
                estacion.localidad
                not in localidades_criticas
            ):
                localidades_criticas.append(
                    estacion.localidad
                )

        matriz_floyd = floyd(
            matriz_adyacencia
        )

        recorrido, kilometros = plan_visitas(
            localidades,
            matriz_floyd,
            "Deán Funes",
            localidades_criticas
        )

        print("\nLocalidades criticas:")

        for localidad in localidades_criticas:
            print("-", localidad)

        print("\nRecorrido:")

        print(" -> ".join(recorrido))

        print(
            f"\nKilometros totales: {kilometros}"
        )