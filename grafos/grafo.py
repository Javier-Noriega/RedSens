import csv
import math
from collections import deque
from pathlib import Path

ruta_csv = Path(__file__).with_name("rutas.csv")
rutas = []

with ruta_csv.open("r", encoding="utf-8-sig", newline="") as archivo:
    lector = csv.reader(archivo, delimiter=";")
    next(lector, None)  # Saltea el encabezado

    for fila in lector:
        origen = fila[0]
        destino = fila[1]
        kilometros = int(fila[2])
        rutas.append((origen, destino, kilometros))

localidades = [
    "Córdoba",
    "Villa Carlos Paz",
    "Alta Gracia",
    "Jesús María",
    "Río Tercero",
    "Villa María",
    "San Francisco",
    "Cosquín",
    "La Falda",
    "Deán Funes",
    "Villa Dolores",
    "Río Cuarto"
]

cantidad = len(localidades)

# Una lista de vecinos por cada localidad
lista_adyacencia = [[] for _ in localidades]

# Una matriz de cantidad x cantidad
matriz_adyacencia = [
    [math.inf for _ in localidades]
    for _ in localidades
]

# La distancia de una localidad a sí misma es cero
for i in range(cantidad):
    matriz_adyacencia[i][i] = 0

# Cargamos cada ruta en las dos representaciones
for origen, destino, kilometros in rutas:
    indice_origen = localidades.index(origen)
    indice_destino = localidades.index(destino)

    # La ruta se agrega en ambos sentidos porque el grafo no es dirigido
    lista_adyacencia[indice_origen].append((indice_destino, kilometros))
    lista_adyacencia[indice_destino].append((indice_origen, kilometros))

    matriz_adyacencia[indice_origen][indice_destino] = kilometros
    matriz_adyacencia[indice_destino][indice_origen] = kilometros

# Algoritmo BFS
def bfs(localidades, lista_adyacencia, nombre_origen):
    cantidad = len(localidades)
    indice_origen = localidades.index(nombre_origen)

    distancias = [-1] * cantidad
    distancias[indice_origen] = 0

    cola = deque([indice_origen])

    while cola:
        actual = cola.popleft()

        for vecino, kilometros in lista_adyacencia[actual]:
            if distancias[vecino] == -1:
                distancias[vecino] = distancias[actual] + 1
                cola.append(vecino)

    return distancias

def mostrar_bfs_desde(origen):
    niveles = bfs(localidades, lista_adyacencia, origen)

    print(f"\nBFS desde {origen}:")
    nivel_maximo = max(niveles)

    for nivel in range(1, nivel_maximo + 1):
        print(f"A {nivel} tramo(s):")
        for i in range(len(localidades)):
            if niveles[i] == nivel:
                print("-", localidades[i])

    inalcanzables = []
    for i in range(len(localidades)):
        if niveles[i] == -1:
            inalcanzables.append(localidades[i])

    if inalcanzables:
        print("No alcanzables:", ", ".join(inalcanzables))

# Algoritmo DFS
def dfs(localidades, lista_adyacencia, nombre_origen, ruta_cortada=None):
    cantidad = len(localidades)
    indice_origen = localidades.index(nombre_origen)

    visitadas = [False] * cantidad
    pila = [indice_origen]
    orden_visita = []

    indice_corte_a = -1
    indice_corte_b = -1

    if ruta_cortada is not None:
        indice_corte_a = localidades.index(ruta_cortada[0])
        indice_corte_b = localidades.index(ruta_cortada[1])

    while pila:
        actual = pila.pop()

        if visitadas[actual]:
            continue

        visitadas[actual] = True
        orden_visita.append(actual)

        for vecino, kilometros in lista_adyacencia[actual]:
            es_ruta_cortada = (
                actual == indice_corte_a and vecino == indice_corte_b
            ) or (
                actual == indice_corte_b and vecino == indice_corte_a
            )

            if es_ruta_cortada:
                continue

            if not visitadas[vecino]:
                pila.append(vecino)

    return orden_visita

# Algoritmo Dijkstra
def dijkstra(localidades, lista_adyacencia, nombre_origen):
    cantidad = len(localidades)
    indice_origen = localidades.index(nombre_origen)

    distancias = [math.inf] * cantidad
    predecesores = [-1] * cantidad
    visitadas = [False] * cantidad

    distancias[indice_origen] = 0

    while True:
        actual = -1
        menor_distancia = math.inf

        for i in range(cantidad):
            if not visitadas[i] and distancias[i] < menor_distancia:
                actual = i
                menor_distancia = distancias[i]

        if actual == -1:
            break

        visitadas[actual] = True

        for vecino, kilometros in lista_adyacencia[actual]:
            nueva_distancia = distancias[actual] + kilometros

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = actual

    return distancias, predecesores


def reconstruir_camino(localidades, indice_origen, indice_destino, predecesores):
    camino = []
    actual = indice_destino

    while actual != -1:
        camino.append(localidades[actual])

        if actual == indice_origen:
            break

        actual = predecesores[actual]

    camino.reverse()
    return camino

# Algoritmo Floyd
def floyd(matriz_adyacencia):
    cantidad = len(matriz_adyacencia)

    # Copiamos la matriz para conservar la original
    distancias = [fila[:] for fila in matriz_adyacencia]

    for intermedia in range(cantidad):
        for origen in range(cantidad):
            for destino in range(cantidad):
                distancia_nueva = (
                    distancias[origen][intermedia]
                    + distancias[intermedia][destino]
                )

                if distancia_nueva < distancias[origen][destino]:
                    distancias[origen][destino] = distancia_nueva

    return distancias


def mostrar_matriz_distancias(localidades, matriz, titulo):
    print(f"\n{titulo}")
    print(f"{'Localidad':20}", end="")

    for localidad in localidades:
        print(f"{localidad[:10]:>12}", end="")

    print()

    for i in range(len(localidades)):
        print(f"{localidades[i]:20}", end="")

        for j in range(len(localidades)):
            valor = matriz[i][j]

            if valor == math.inf:
                print(f"{'-':>12}", end="")
            else:
                print(f"{valor:>12}", end="")

        print()

# Plan de Visitas
def plan_visitas(localidades, distancias_floyd, nombre_base, localidades_criticas):
    indice_base = localidades.index(nombre_base)
    pendientes = []

    # Validamos los nombres y quitamos localidades repetidas
    for localidad in localidades_criticas:
        if localidad not in localidades:
            raise ValueError(f"Localidad desconocida: {localidad}")

        if localidad != nombre_base and localidad not in pendientes:
            pendientes.append(localidad)

    recorrido = [nombre_base]
    kilometros_totales = 0
    indice_actual = indice_base

    while pendientes:
        siguiente = pendientes[0]
        indice_siguiente = localidades.index(siguiente)
        menor_distancia = distancias_floyd[indice_actual][indice_siguiente]

        # Elegimos la localidad pendiente más cercana
        for localidad in pendientes[1:]:
            indice = localidades.index(localidad)
            distancia = distancias_floyd[indice_actual][indice]

            if distancia < menor_distancia:
                siguiente = localidad
                indice_siguiente = indice
                menor_distancia = distancia

        recorrido.append(siguiente)
        kilometros_totales += menor_distancia
        pendientes.remove(siguiente)
        indice_actual = indice_siguiente

    # Regresamos a la base
    if len(recorrido) > 1:
        kilometros_totales += distancias_floyd[indice_actual][indice_base]
        recorrido.append(nombre_base)

    return recorrido, kilometros_totales

def menu_m3(estaciones_criticas=None):
    while True:
        print("\n=== M3: Red vial ===")
        print("1. Ver localidades cargadas")
        print("2. Ver lista de adyacencia")
        print("3. Ver matriz de adyacencia")
        print("4. BFS desde Deán Funes o localidad elegida")
        print("5. DFS y conectividad")
        print("6. Dijkstra desde Deán Funes")
        print("7. Floyd")
        print("8. Simular plan de visitas")
        print("0. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            print(f"\nLocalidades cargadas: {len(localidades)}")
            for localidad in localidades:
                print("-", localidad)

        elif opcion == "2":
            print("\nLista de adyacencia:")
            for i in range(len(localidades)):
                print(localidades[i], "->", end=" ")

                for vecino, kilometros in lista_adyacencia[i]:
                    print(
                        f"{localidades[vecino]} ({kilometros} km)",
                        end="; "
                    )

                print()

        elif opcion == "3":
            mostrar_matriz_distancias(
                localidades,
                matriz_adyacencia,
                "Matriz de adyacencia:"
            )

        elif opcion == "4":
            while True:
                print("\n=== BFS por localidad ===")
                print("1. Desde la base: Deán Funes")
                print("2. Escribir otra localidad")
                print("0. Volver al menú M3")

                seleccion = input("Elegí una opción: ").strip()

                if seleccion == "0":
                    break
                elif seleccion == "1":
                    origen = "Deán Funes"
                elif seleccion == "2":
                    origen = input(
                        "Escribí el nombre de la localidad: "
                    ).strip()
                else:
                    print("Opción no válida.")
                    continue

                if origen not in localidades:
                    print("Esa localidad no está en la red.")
                    continue

                mostrar_bfs_desde(origen)

        elif opcion == "5":
            recorrido = dfs(localidades, lista_adyacencia, "Deán Funes")
            print("\nDFS desde Deán Funes:")
            for indice in recorrido:
                print("-", localidades[indice])

            if len(recorrido) == len(localidades):
                print("La red es conexa.")

            recorrido_cortado = dfs(
                localidades,
                lista_adyacencia,
                "Deán Funes",
                ("Deán Funes", "Jesús María")
            )

            print("\nAl cortar Deán Funes - Jesús María:")
            if len(recorrido_cortado) == len(localidades):
                print("La red sigue conectada.")
            else:
                print("La red queda desconectada.")

        elif opcion == "6":
            distancias, predecesores = dijkstra(
                localidades,
                lista_adyacencia,
                "Deán Funes"
            )
            indice_base = localidades.index("Deán Funes")

            print("\nDijkstra desde Deán Funes:")
            for destino in range(len(localidades)):
                camino = reconstruir_camino(
                    localidades,
                    indice_base,
                    destino,
                    predecesores
                )
                print(
                    f"{localidades[destino]}: {distancias[destino]} km"
                    f" | Camino: {' -> '.join(camino)}"
                )

        elif opcion == "7":
            resultado = floyd(matriz_adyacencia)
            mostrar_matriz_distancias(
                localidades,
                resultado,
                "Matriz de distancias mínimas de Floyd:"
            )

        elif opcion == "8":
            if estaciones_criticas is None:
                print("\nM2 todavía no entregó las estaciones críticas.")
                continue

            localidades_criticas = []

            for estacion in estaciones_criticas:
                localidad = estacion.localidad

                if localidad not in localidades_criticas:
                    localidades_criticas.append(localidad)

            distancias_floyd = floyd(matriz_adyacencia)

            recorrido, kilometros = plan_visitas(
                localidades,
                distancias_floyd,
                "Deán Funes",
                localidades_criticas
            )

            print("\nLocalidades críticas:")
            for localidad in localidades_criticas:
                print("-", localidad)

            print("\nOrden sugerido:")
            print(" -> ".join(recorrido))
            print("Kilómetros totales:", kilometros)
            print("El criterio de vecino más cercano no garantiza el recorrido óptimo.")

        elif opcion == "0":
            print("Saliste del Módulo 3.")
            break

        else:
            print("Opción no válida. Elegí un número del 0 al 8.")


if __name__ == "__main__":
    menu_m3()
