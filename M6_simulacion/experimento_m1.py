import random

from M6_simulacion.generador_estaciones import GeneradorEstaciones
from M1_hash.tabla_hash import Tablahash


# Parametros correspondientes al grupo 5.
SEMILLA = 5026
CANTIDAD_ESTACIONES = 10000
CANTIDAD_BUSQUEDAS = 1000
CAPACIDAD_INICIAL = 23


def crear_muestras_busqueda(estaciones):
    """Crea las mismas muestras aleatorias para comparar ambas estrategias.

    Las busquedas exitosas se toman al azar de las estaciones insertadas.
    Las no exitosas se toman al azar de un rango amplio de sufijos que no
    fueron generados, y no solamente de los mil codigos inmediatos siguientes.
    """
    cantidad = min(CANTIDAD_BUSQUEDAS, len(estaciones))
    rnd = random.Random(SEMILLA + 1)

    exitosas = [
        estacion.codigo
        for estacion in rnd.sample(estaciones, cantidad)
    ]

    # El generador produce sufijos 1..CANTIDAD_ESTACIONES. Tomamos
    # candidatos de un rango amplio posterior, sin utilizar set/dict ni
    # ninguna estructura que reemplace a la tabla hash del ejercicio.
    limite_superior = max(100000, CANTIDAD_ESTACIONES * 10)
    sufijos_ausentes = rnd.sample(
        range(CANTIDAD_ESTACIONES + 1, limite_superior + 1),
        cantidad
    )
    no_exitosas = [f"CBA-{numero:04d}" for numero in sufijos_ausentes]

    return exitosas, no_exitosas


def medir_promedio_sondeos(tabla, codigos, debe_existir):
    total_sondeos = 0

    for codigo in codigos:
        resultado, sondeos = tabla.buscar_con_sondeos(codigo)
        total_sondeos += sondeos

        if debe_existir and resultado is None:
            raise AssertionError(
                f"La busqueda exitosa no encontro el codigo {codigo}."
            )

        if not debe_existir and resultado is not None:
            raise AssertionError(
                f"La busqueda no exitosa encontro un codigo inexistente: {codigo}."
            )

    if not codigos:
        return 0.0

    return total_sondeos / len(codigos)


class ResultadoEstrategia:
    """Agrupa las metricas sin utilizar diccionarios como estructura de datos."""

    def __init__(
        self, estrategia, insertadas, colisiones_insercion, sondeos_insercion,
        colisiones_rehash, sondeos_rehash, tiempo_rehash_ms,
        promedio_exitosas, promedio_no_exitosas, rehashes,
        capacidad_final, factor_carga_final
    ):
        self.estrategia = estrategia
        self.insertadas = insertadas
        self.colisiones_insercion = colisiones_insercion
        self.sondeos_insercion = sondeos_insercion
        self.colisiones_rehash = colisiones_rehash
        self.sondeos_rehash = sondeos_rehash
        self.tiempo_rehash_ms = tiempo_rehash_ms
        self.promedio_exitosas = promedio_exitosas
        self.promedio_no_exitosas = promedio_no_exitosas
        self.rehashes = rehashes
        self.capacidad_final = capacidad_final
        self.factor_carga_final = factor_carga_final


def ejecutar_estrategia(estaciones, estrategia, codigos_exitosos, codigos_no_exitosos):
    tabla = Tablahash(CAPACIDAD_INICIAL, estrategia)

    insertadas = 0
    for estacion in estaciones:
        if tabla.insertar(estacion):
            insertadas += 1
        else:
            raise AssertionError(
                f"No se pudo insertar {estacion.codigo}; puede estar duplicada."
            )

    if insertadas != len(estaciones):
        raise AssertionError("La cantidad insertada no coincide con la esperada.")

    promedio_exitosas = medir_promedio_sondeos(
        tabla,
        codigos_exitosos,
        debe_existir=True
    )
    promedio_no_exitosas = medir_promedio_sondeos(
        tabla,
        codigos_no_exitosos,
        debe_existir=False
    )

    return ResultadoEstrategia(
        estrategia=estrategia,
        insertadas=insertadas,
        colisiones_insercion=tabla.colisiones_insercion,
        sondeos_insercion=tabla.sondeos_insercion,
        colisiones_rehash=tabla.colisiones_rehash,
        sondeos_rehash=tabla.sondeos_rehash,
        tiempo_rehash_ms=tabla.tiempo_rehash_ns / 1_000_000,
        promedio_exitosas=promedio_exitosas,
        promedio_no_exitosas=promedio_no_exitosas,
        rehashes=tabla.rehashes,
        capacidad_final=tabla.capacidad,
        factor_carga_final=tabla.factor_carga(),
    )


def mostrar_resultado(resultado):
    print("\nSONDEO", resultado.estrategia.upper())
    print("Estaciones insertadas              :", resultado.insertadas)
    print("Colisiones durante insercion       :", resultado.colisiones_insercion)
    print("Sondeos durante insercion          :", resultado.sondeos_insercion)
    print("Colisiones durante rehash          :", resultado.colisiones_rehash)
    print("Sondeos durante rehash             :", resultado.sondeos_rehash)
    print("Tiempo acumulado de rehash         :", f"{resultado.tiempo_rehash_ms:.3f} ms")
    print("Promedio busqueda exitosa          :", f"{resultado.promedio_exitosas:.3f}")
    print("Promedio busqueda no exitosa       :", f"{resultado.promedio_no_exitosas:.3f}")
    print("Rehashings                         :", resultado.rehashes)
    print("Capacidad final                    :", resultado.capacidad_final)
    print("Factor de carga final              :", f"{resultado.factor_carga_final:.4f}")


def ejecutar():
    print("\n========================================")
    print(" EXPERIMENTO M1 - TABLAS HASH")
    print("========================================")

    generador = GeneradorEstaciones(SEMILLA)
    estaciones = generador.generar_estaciones(CANTIDAD_ESTACIONES)

    # Se conserva el conjunto de claves, pero se aleatoriza el orden de insercion.
    random.Random(SEMILLA).shuffle(estaciones)

    codigos_exitosos, codigos_no_exitosos = crear_muestras_busqueda(estaciones)

    print("Estaciones a insertar                 :", len(estaciones))
    print("Busquedas exitosas por estrategia     :", len(codigos_exitosos))
    print("Busquedas no exitosas por estrategia  :", len(codigos_no_exitosos))
    print("Semilla                               :", SEMILLA)
    print("Capacidad inicial                     :", CAPACIDAD_INICIAL)
    print("Umbral de carga comun                 :", Tablahash.UMBRAL_FACTOR_CARGA)
    print("Funcion hash                          : polinomial sobre todo el codigo")

    resultado_lineal = ejecutar_estrategia(
        estaciones,
        Tablahash.SONDEO_LINEAL,
        codigos_exitosos,
        codigos_no_exitosos
    )
    resultado_cuadratica = ejecutar_estrategia(
        estaciones,
        Tablahash.SONDEO_CUADRATICA,
        codigos_exitosos,
        codigos_no_exitosos
    )

    # Al compartir capacidad inicial, cantidad de claves y umbral,
    # ambas tablas deben terminar con igual capacidad y factor de carga.
    if resultado_lineal.capacidad_final != resultado_cuadratica.capacidad_final:
        raise AssertionError("Las estrategias terminaron con capacidades diferentes.")

    if abs(
        resultado_lineal.factor_carga_final
        - resultado_cuadratica.factor_carga_final
    ) > 1e-12:
        raise AssertionError("Las estrategias terminaron con factores de carga diferentes.")

    mostrar_resultado(resultado_lineal)
    mostrar_resultado(resultado_cuadratica)

    print("\n========================================")
    print(" COMPARACION")
    print("========================================")
    print(f"{'Metrica':38} {'Lineal':>14} {'Cuadratica':>14}")
    print("-" * 70)

    filas = [
        ("Colisiones insercion", "colisiones_insercion", 0),
        ("Sondeos insercion", "sondeos_insercion", 0),
        ("Colisiones rehash", "colisiones_rehash", 0),
        ("Sondeos rehash", "sondeos_rehash", 0),
        ("Promedio busqueda exitosa", "promedio_exitosas", 3),
        ("Promedio busqueda no exitosa", "promedio_no_exitosas", 3),
        ("Rehashings", "rehashes", 0),
        ("Capacidad final", "capacidad_final", 0),
        ("Factor de carga final", "factor_carga_final", 4),
        ("Tiempo rehash acumulado (ms)", "tiempo_rehash_ms", 3),
    ]

    for etiqueta, atributo, decimales in filas:
        valor_lineal = getattr(resultado_lineal, atributo)
        valor_cuadratico = getattr(resultado_cuadratica, atributo)

        if decimales:
            formato = f"{{:>{14}.{decimales}f}}"
            texto_lineal = formato.format(valor_lineal)
            texto_cuadratico = formato.format(valor_cuadratico)
        else:
            texto_lineal = f"{valor_lineal:>14}"
            texto_cuadratico = f"{valor_cuadratico:>14}"

        print(f"{etiqueta:38} {texto_lineal} {texto_cuadratico}")

    print("\nNota: las colisiones y sondeos de insercion no incluyen las reinserciones")
    print("del rehash; estas se informan por separado. El tiempo de rehash es")
    print("orientativo y depende del equipo donde se ejecute el experimento.")


if __name__ == "__main__":
    ejecutar()
