from M6_simulacion.generador_estaciones import (
    GeneradorEstaciones
)


def secuencias_iguales():

    gen1 = GeneradorEstaciones(
        5026
    )

    gen2 = GeneradorEstaciones(
        5026
    )

    lista1 = gen1.generar_estaciones(
        5
    )

    lista2 = gen2.generar_estaciones(
        5
    )

    iguales = True

    for i in range(5):

        if (
            lista1[i].localidad
            != lista2[i].localidad
        ):
            iguales = False

    return iguales


def secuencias_distintas():

    gen1 = GeneradorEstaciones(
        5026
    )

    gen2 = GeneradorEstaciones(
        9999
    )

    lista1 = gen1.generar_estaciones(
        5
    )

    lista2 = gen2.generar_estaciones(
        5
    )

    distintas = False

    for i in range(5):

        if (
            lista1[i].localidad
            != lista2[i].localidad
        ):
            distintas = True

    return distintas