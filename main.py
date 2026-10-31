from Modelos.estacion import estacion
from hash.tabla_hash import Tablahash

tablahash = Tablahash(11,"cuadratica")

estacion1 = estacion(
    "CBA-0347",
    347,
    "Embalse Norte",
    "Rio Tercero",
    "METEOROLOGICA",
    18,
    42
)

estacion2 = estacion(
    "CBA-0358",
    358,
    "Embalse Norte",
    "Rio Tercero",
    "METEOROLOGICA",
    18,
    42
)

tablahash.insertar(estacion1)
tablahash.insertar(estacion2)

tablahash.mostrar()

tablahash.mostrar_estadisticas()

encontrada = tablahash.buscar("CBA-0358")

print()
print("Encontrada:")
print(encontrada)