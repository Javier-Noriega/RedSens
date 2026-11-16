from M6_simulacion.generador_estaciones import (
    GeneradorEstaciones
)


def comprobar_uniformidad():

    generador = GeneradorEstaciones(
        5026
    )

    estaciones = (
        generador.generar_estaciones(
            10000
        )
    )

    intervalos = {

        "0-10": 0,
        "11-20": 0,
        "21-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0,
        "61-70": 0,
        "71-80": 0,
        "81-90": 0,
        "91-100": 0
    }

    for estacion in estaciones:

        b = estacion.bateria

        if b <= 10:
            intervalos["0-10"] += 1

        elif b <= 20:
            intervalos["11-20"] += 1

        elif b <= 30:
            intervalos["21-30"] += 1

        elif b <= 40:
            intervalos["31-40"] += 1

        elif b <= 50:
            intervalos["41-50"] += 1

        elif b <= 60:
            intervalos["51-60"] += 1

        elif b <= 70:
            intervalos["61-70"] += 1

        elif b <= 80:
            intervalos["71-80"] += 1

        elif b <= 90:
            intervalos["81-90"] += 1

        else:
            intervalos["91-100"] += 1

    return intervalos