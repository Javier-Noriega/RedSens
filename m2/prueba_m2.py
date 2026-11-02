import random
import time

from .abb import ABB
from .avl import AVL
from Modelos.estacion import estacion

SEMILLA = 1026   # <-- cambiar por la semilla de tu grupo

def est(n, bateria):
    return estacion(f"CBA-{n:04d}", n, f"Estacion {n}", "Rio Tercero",
                    "METEOROLOGICA", bateria, 0)
def nums(lista):
    return [e.numero for e in lista]
def demo():
    print("=== DEMO: insertar 10, 20, 30 ===")
    abb, avl = ABB(), AVL()
    for n in (10, 20, 30):
        abb.insertar(est(n, 50))
        avl.insertar(est(n, 50))
    print("ABB preorden", nums(abb.preorden()), "altura =", abb.altura())
    print("AVL preorden", nums(avl.preorden()), "altura =", avl.altura(),
        " (rotación simple a la izquierda)")
    print("\n=== DEMO: AVL con 20 estaciones ===")
    rnd = random.Random(SEMILLA)
    idx = AVL()
    for n in range(1, 21):
        idx.insertar(est(n, rnd.randint(0, 100)))
    print("inorden  ", nums(idx.inorden()))
    print("preorden ", nums(idx.preorden()))
    print("postorden", nums(idx.postorden()))
    print("nodos =", idx.cantidad_nodos(), "hojas =", idx.cantidad_hojas(),
        "altura =", idx.altura())
    print("rango [5,12]:", nums(idx.rango(5, 12)))
    print("críticas (bat<20):", nums(idx.criticas()))
    print("eliminar 10 ->", idx.eliminar(10), ", eliminar 99 ->", idx.eliminar(99))
    print("inorden  ", nums(idx.inorden()))
def tiempo_busqueda(arbol, claves):
    """Promedio en ns de buscar todas las claves (con una pasada de calentamiento)."""
    for k in claves:
        arbol.buscar(k)
    ini = time.perf_counter_ns()
    for k in claves:
        arbol.buscar(k)
    fin = time.perf_counter_ns()
    return (fin - ini) / len(claves)
def experimento():
    for ordenado in (True, False):
        print("\n=== EXPERIMENTO: inserción", "ASCENDENTE" if ordenado else "ALEATORIA", "===")
        print(f"{'N':<8} | {'ABB altura':<11}{'ABB busq (ns)':<15}| {'AVL altura':<11}{'AVL busq (ns)':<15}")
        for n in (1000, 5000, 10000):
            rnd = random.Random(SEMILLA)
            claves = list(range(1, n + 1))
            if not ordenado:
                rnd.shuffle(claves)
            estaciones = [est(k, rnd.randint(0, 100)) for k in claves]
            abb, avl = ABB(), AVL()
            for e in estaciones:
                abb.insertar(e)
                avl.insertar(e)
            print(f"{n:<8} | {abb.altura_iterativa():<11}{tiempo_busqueda(abb, claves):<15.1f}"
                f"| {avl.altura_iterativa():<11}{tiempo_busqueda(avl, claves):<15.1f}")
def main():
    demo()
    experimento()
if __name__ == "__main__":
    # Con las claves ordenadas el ABB queda con 10.000 niveles. Para que el experimento
    # no dé RecursionError, la inserción, la búsqueda y la altura del experimento son
    # iterativas (no hace falta tocar el límite de recursión de Python).
    main()