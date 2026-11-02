

from collections import deque
from time import perf_counter_ns


def josephus_simple(n, m):
    tecnicos = deque(range(1, n + 1))
    guardias = []

    while len(tecnicos) > 1:
        tecnicos.rotate(-m)
        seleccionado = tecnicos.popleft()
        guardias.append(seleccionado)

    return guardias, tecnicos[0]


class Nodo:
    def __init__(self, numero, izquierdo=None, derecho=None):
        self.numero = numero
        self.izquierdo = izquierdo
        self.derecho = derecho
        self.activo = True
        self.vivos = 1

        if izquierdo:
            self.vivos += izquierdo.vivos
        if derecho:
            self.vivos += derecho.vivos


def crear_arbol(inicio, fin):
    if inicio > fin:
        return None

    medio = (inicio + fin) // 2
    izquierdo = crear_arbol(inicio, medio - 1)
    derecho = crear_arbol(medio + 1, fin)

    return Nodo(medio, izquierdo, derecho)


def retirar_por_posicion(nodo, posicion):
    vivos_izquierda = nodo.izquierdo.vivos if nodo.izquierdo else 0

    if posicion < vivos_izquierda:
        seleccionado = retirar_por_posicion(nodo.izquierdo, posicion)
    elif nodo.activo and posicion == vivos_izquierda:
        nodo.activo = False
        seleccionado = nodo.numero
    else:
        desplazamiento = vivos_izquierda + (1 if nodo.activo else 0)
        seleccionado = retirar_por_posicion(nodo.derecho, posicion - desplazamiento)

    nodo.vivos -= 1
    return seleccionado


def josephus_arbol(n, m):
    raiz = crear_arbol(1, n)
    guardias = []
    posicion = 0
    restantes = n

    while restantes > 1:
        posicion = (posicion + m) % restantes
        guardias.append(retirar_por_posicion(raiz, posicion))
        restantes -= 1
        posicion %= restantes

    suplente = retirar_por_posicion(raiz, 0)
    return guardias, suplente


def mostrar_calendario(numero_grupo):
    m_grupo = (numero_grupo - 1) % 4 + 1
    guardias, suplente = josephus_arbol(12, m_grupo)

    assert (guardias, suplente) == josephus_simple(12, m_grupo)

    print(f"\nCalendario de guardias - Grupo {numero_grupo} (M = {m_grupo})")
    for fin_de_semana, tecnico in enumerate(guardias, start=1):
        print(f"Fin de semana {fin_de_semana}: Tecnico {tecnico}")
    print(f"Suplente de emergencias: Tecnico {suplente}")

    return m_grupo


def medir_tiempo(funcion, n, m):
    inicio = perf_counter_ns()
    resultado = funcion(n, m)
    tiempo = perf_counter_ns() - inicio
    return resultado, tiempo


def comparar_rendimiento(m_grupo):
    for m in (m_grupo, 1000):
        print(f"\nComparacion de tiempos con M = {m}")
        print("Tecnicos | Simple (ms) | Arbol (ms)")

        for n in (1000, 10000, 100000):
            resultado_simple, tiempo_simple = medir_tiempo(josephus_simple, n, m)
            resultado_arbol, tiempo_arbol = medir_tiempo(josephus_arbol, n, m)

            assert resultado_simple == resultado_arbol
            print(f"{n:>8} | {tiempo_simple / 1_000_000:>11.3f} | {tiempo_arbol / 1_000_000:>10.3f}")


def ejecutar_m5():
    guardias_simple, suplente_simple = josephus_simple(5, 1)
    guardias_arbol, suplente_arbol = josephus_arbol(5, 1)

    print("Solucion simple:", guardias_simple, "- Suplente:", suplente_simple)
    print("Solucion con arbol:", guardias_arbol, "- Suplente:", suplente_arbol)

    assert guardias_simple == [2, 4, 1, 5]
    assert suplente_simple == 3
    assert (guardias_simple, suplente_simple) == (guardias_arbol, suplente_arbol)
    print("Las dos implementaciones coinciden.")

    numero_grupo = int(input("\nNumero de grupo (1 al 15): "))

    if 1 <= numero_grupo <= 15:
        m_grupo = mostrar_calendario(numero_grupo)
        comparar_rendimiento(m_grupo)
    else:
        print("El numero de grupo debe estar entre 1 y 15.")


if __name__ == "__main__":
    ejecutar_m5()

