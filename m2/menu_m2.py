import random

from Modelos.estacion import estacion
from . import prueba_m2
from .avl import AVL

LOCALIDADES = [
    "Córdoba", "Villa Carlos Paz", "Alta Gracia", "Jesús María",
    "Río Tercero", "Villa María", "San Francisco", "Cosquín",
    "La Falda", "Deán Funes", "Villa Dolores", "Río Cuarto",
]


def _leer_entero(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        print("Tenés que escribir un número entero.")
        return None

def _mostrar(lista):
    if not lista:
        print("No hay estaciones para mostrar.")
        return
    for e in lista:
        print(f"{e.codigo} | {e.nombre} | {e.localidad} | bat={e.bateria}%")
    print(f"Total: {len(lista)}")


def cargar_demo(avl, cantidad=50, semilla=prueba_m2.SEMILLA):
    """Carga estaciones simuladas (solo para probar el M2 por separado)."""
    rnd = random.Random(semilla)
    for n in range(1, cantidad + 1):
        avl.insertar(estacion(f"CBA-{n:04d}", n, f"Estacion {n}",
                            rnd.choice(LOCALIDADES), "METEOROLOGICA",
                            rnd.randint(0, 100), rnd.randint(0, 90)))


def menu_m2(avl):
    """Menú del M2. Recibe el AVL con las estaciones ya cargadas."""
    while True:
        print("\n=== M2: Índice ordenado (AVL) ===")
        print("1. Listar estaciones por rango de números")
        print("2. Reporte de estaciones críticas (batería < 20)")
        print("3. Buscar estación por número")
        print("4. Ver altura, cantidad de nodos y hojas")
        print("5. Plan de visitas con las críticas (M3)")
        print("6. Ejecutar experimento ABB vs AVL")
        print("0. Volver")
        opcion = input("Elegí una opción: ")
        if opcion == "1":
            a = _leer_entero("Desde el número: ")
            b = _leer_entero("Hasta el número: ")
            if a is not None and b is not None:
                _mostrar(avl.rango(a, b))
        elif opcion == "2":
            _mostrar(avl.criticas())
        elif opcion == "3":
            n = _leer_entero("Número de estación: ")
            if n is not None:
                e = avl.buscar(n)
                print(e if e is None else
                    f"{e.codigo} | {e.nombre} | {e.localidad} | bat={e.bateria}%")
        elif opcion == "4":
            print("Altura:", avl.altura())
            print("Nodos:", avl.cantidad_nodos())
            print("Hojas:", avl.cantidad_hojas())
        elif opcion == "5":
            try:
                from grafos.grafo import menu_m3
            except ImportError:
                print("No se encontró el módulo M3 (grafos/grafo.py).")
                continue
            menu_m3(avl.criticas())
        elif opcion == "6":
            prueba_m2.experimento()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Elegí un número del 0 al 6.")
if __name__ == "__main__":
    indice = AVL()
    cargar_demo(indice)
    menu_m2(indice)