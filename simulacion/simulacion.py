import random
import time

# Semilla asignada al grupo 5
SEMILLA_GRUPO = 5026


def generar_secuencia(semilla, cantidad=10):
    generador = random.Random(semilla)
    return [generador.randint(1, 100) for _ in range(cantidad)]


def secuencias_iguales(semilla):
    """Comprueba que dos generadores con la misma semilla repiten la secuencia."""
    secuencia_1 = generar_secuencia(semilla)
    secuencia_2 = generar_secuencia(semilla)

    son_iguales = secuencia_1 == secuencia_2

    print("--- Secuencias con la misma semilla ---")
    print("Generador 1:", secuencia_1)
    print("Generador 2:", secuencia_2)
    print("¿Son iguales?", son_iguales)

    return son_iguales


def secuencias_distintas(semilla_1, semilla_2):
    """Comprueba que las secuencias de estas dos semillas sean distintas."""
    if semilla_1 == semilla_2:
        raise ValueError("Para esta comprobación, las semillas deben ser distintas.")

    secuencia_1 = generar_secuencia(semilla_1)
    secuencia_2 = generar_secuencia(semilla_2)

    son_distintas = secuencia_1 != secuencia_2

    print("\n--- Secuencias con semillas distintas ---")
    print(f"Semilla {semilla_1}:", secuencia_1)
    print(f"Semilla {semilla_2}:", secuencia_2)
    print("¿Son distintas?", son_distintas)

    return son_distintas


def comprueba_uniformidad(semilla, n_muestras=100000):
    """Cuenta baterías entre 0 y 100 y compara cada intervalo con lo esperado."""
    if n_muestras <= 0:
        raise ValueError("La cantidad de muestras debe ser mayor que cero.")

    generador = random.Random(semilla)

    # Diez intervalos contienen 10 valores; el último contiene solo el valor 100.
    intervalos = [0] * 11

    for _ in range(n_muestras):
        bateria = generador.randint(0, 100)
        indice = min(bateria // 10, 10)
        intervalos[indice] += 1

    print("\n--- Uniformidad de baterías (0 a 100) ---")
    print("Muestras totales:", n_muestras)
    print(f"{'Intervalo':<15} | {'Observado':>10} | {'Esperado':>10} | {'Diferencia':>12}")
    print("-" * 58)

    for indice, observadas in enumerate(intervalos):
        minimo = indice * 10
        maximo = min(minimo + 9, 100)
        cantidad_valores = maximo - minimo + 1

        # Hay 101 valores posibles: del 0 al 100, inclusive.
        esperado = n_muestras * cantidad_valores / 101
        diferencia = ((observadas - esperado) / esperado) * 100

        etiqueta = f"{minimo} a {maximo}"
        print(
            f"{etiqueta:<15} | {observadas:>10} | "
            f"{esperado:>10.1f} | {diferencia:>+11.2f}%"
        )

    print("\nLas diferencias pueden variar por azar; se comparan con los valores esperados.")
    return intervalos


def medir_tiempo_ns(funcion, *argumentos, **opciones):
    """Mide una ejecución real y devuelve su resultado y el tiempo en nanosegundos."""
    inicio = time.perf_counter_ns()
    resultado = funcion(*argumentos, **opciones)
    tiempo_ns = time.perf_counter_ns() - inicio
    return resultado, tiempo_ns


def medir_tiempos_rendimiento(experimentos):
    """
    Recibe experimentos reales como tuplas:
    (nombre, funcion, argumentos, opciones)
    """
    print("\n--- Medición de experimentos ---")
    print(f"{'Experimento':<25} | {'Tiempo (ns)':>15} | {'Tiempo (ms)':>12}")
    print("-" * 60)

    resultados = []

    for nombre, funcion, argumentos, opciones in experimentos:
        resultado, tiempo_ns = medir_tiempo_ns(
            funcion,
            *argumentos,
            **opciones
        )

        tiempo_ms = tiempo_ns / 1_000_000
        print(f"{nombre:<25} | {tiempo_ns:>15} | {tiempo_ms:>12.4f}")
        resultados.append((nombre, resultado, tiempo_ns))

    return resultados


if __name__ == "__main__":
    secuencias_iguales(SEMILLA_GRUPO)
    secuencias_distintas(SEMILLA_GRUPO, SEMILLA_GRUPO + 1)
    comprueba_uniformidad(SEMILLA_GRUPO)
    print("INICIANDO PRUEBAS DEL MODULO 6\n")
    secuencias_iguales(SEMILLA_GRUPO)
    secuencias_distintas(SEMILLA_GRUPO, SEMILLA_GRUPO + 1)
    comprueba_uniformidad(SEMILLA_GRUPO)
    medir_tiempos_rendimiento()
