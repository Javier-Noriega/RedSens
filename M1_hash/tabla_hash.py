from time import perf_counter_ns


class Tablahash:
    """Tabla hash propia con direccionamiento abierto.

    La estrategia cuadratica usa h(k) + i**2. Para una capacidad prima,
    esta secuencia visita (capacidad + 1) // 2 posiciones distintas.
    Por eso se utiliza un factor de carga maximo comun de 0.50.
    """

    SONDEO_LINEAL = "lineal"
    SONDEO_CUADRATICA = "cuadratica"
    BORRADO = object()
    UMBRAL_FACTOR_CARGA = 0.50

    def __init__(self, capacidad, SONDEO):
        if SONDEO not in (self.SONDEO_LINEAL, self.SONDEO_CUADRATICA):
            raise ValueError(f"Estrategia de sondeo invalida: {SONDEO}")

        if not isinstance(capacidad, int) or capacidad < 3:
            raise ValueError("La capacidad debe ser un entero mayor o igual a 3.")

        if not self.es_primo(capacidad):
            raise ValueError(
                "La capacidad inicial debe ser prima para utilizar sondeo cuadratico."
            )

        self.capacidad = capacidad
        self.tabla = [None] * capacidad
        self.elementos = 0
        self.borrados = 0
        self.SONDEO = SONDEO

        # Metricas separadas para no mezclar inserciones, busquedas y rehash.
        self.colisiones_insercion = 0
        self.sondeos_insercion = 0
        self.colisiones_rehash = 0
        self.sondeos_rehash = 0
        self.sondeos_busqueda = 0
        self.sondeos_eliminacion = 0
        self.rehashes = 0
        self.tiempo_rehash_ns = 0

    @property
    def colisiones(self):
        """Compatibilidad: total de colisiones de insercion y rehash."""
        return self.colisiones_insercion + self.colisiones_rehash

    @property
    def sondeos(self):
        """Compatibilidad: total de sondeos registrados en todas las operaciones."""
        return (
            self.sondeos_insercion
            + self.sondeos_rehash
            + self.sondeos_busqueda
            + self.sondeos_eliminacion
        )

    def funcionhash(self, codigo):
        """Hash polinomial deterministico que considera todos los caracteres.

        No se utiliza hash() de Python porque su resultado puede cambiar
        entre procesos. El calculo modular mantiene el valor dentro de la tabla.
        """
        if not isinstance(codigo, str) or not codigo:
            raise ValueError("El codigo de la estacion debe ser un texto no vacio.")

        valor = 0
        for caracter in codigo:
            valor = (valor * 31 + ord(caracter)) % self.capacidad
        return valor

    def calcularindice(self, hashbase, intento):
        if self.SONDEO == self.SONDEO_LINEAL:
            return (hashbase + intento) % self.capacidad

        return (hashbase + intento * intento) % self.capacidad

    def _max_sondeos(self):
        if self.SONDEO == self.SONDEO_LINEAL:
            return self.capacidad

        # Para capacidad prima, los primeros ceil(capacidad / 2)
        # valores de i**2 producen posiciones distintas.
        return (self.capacidad + 1) // 2

    def _localizar_para_insertar(self, codigo, durante_rehash=False):
        """Devuelve (posicion_libre, elemento_existente).

        Continúa después de un BORRADO para no insertar una clave duplicada
        que pudiera encontrarse más adelante en la secuencia de sondeo.
        """
        hashbase = self.funcionhash(codigo)
        primer_borrado = None
        sondeos = 0
        colisiones = 0

        for intento in range(self._max_sondeos()):
            indice = self.calcularindice(hashbase, intento)
            sondeos += 1
            actual = self.tabla[indice]

            if actual is None:
                self._acumular_metricas_insercion(
                    sondeos, colisiones, durante_rehash
                )
                if primer_borrado is not None:
                    return primer_borrado, None
                return indice, None

            if actual is self.BORRADO:
                if primer_borrado is None:
                    primer_borrado = indice
                continue

            if actual.codigo == codigo:
                self._acumular_metricas_insercion(
                    sondeos, colisiones, durante_rehash
                )
                return None, actual

            # Una celda ocupada por otra clave representa una colision.
            colisiones += 1

        self._acumular_metricas_insercion(sondeos, colisiones, durante_rehash)
        return primer_borrado, None

    def _acumular_metricas_insercion(self, sondeos, colisiones, durante_rehash):
        if durante_rehash:
            self.sondeos_rehash += sondeos
            self.colisiones_rehash += colisiones
        else:
            self.sondeos_insercion += sondeos
            self.colisiones_insercion += colisiones

    def insertar(self, estacion):
        """Inserta una estacion; devuelve False si el codigo ya existe."""
        if not hasattr(estacion, "codigo"):
            raise ValueError("La estacion debe tener el atributo 'codigo'.")

        while True:
            indice, existente = self._localizar_para_insertar(estacion.codigo)

            if existente is not None:
                return False

            factor_proyectado = (self.elementos + 1) / self.capacidad

            # Si se excede el umbral comun, se amplia antes de guardar.
            # Tambien se amplia si no hay ninguna posicion alcanzable libre.
            if (
                factor_proyectado > self.umbral_factor_carga()
                or indice is None
            ):
                self.rehash()
                continue

            celda_anterior = self.tabla[indice]
            self.tabla[indice] = estacion
            self.elementos += 1

            if celda_anterior is self.BORRADO:
                self.borrados -= 1

            return True

    def buscar_con_sondeos(self, codigo):
        """Devuelve (estacion_o_None, cantidad_de_sondeos) sin alterar contadores."""
        hashbase = self.funcionhash(codigo)
        sondeos = 0

        for intento in range(self._max_sondeos()):
            indice = self.calcularindice(hashbase, intento)
            sondeos += 1
            actual = self.tabla[indice]

            if actual is None:
                return None, sondeos

            if actual is not self.BORRADO and actual.codigo == codigo:
                return actual, sondeos

        return None, sondeos

    def buscar(self, codigo):
        resultado, sondeos = self.buscar_con_sondeos(codigo)
        self.sondeos_busqueda += sondeos
        return resultado

    def eliminar(self, codigo):
        hashbase = self.funcionhash(codigo)

        for intento in range(self._max_sondeos()):
            indice = self.calcularindice(hashbase, intento)
            self.sondeos_eliminacion += 1
            actual = self.tabla[indice]

            if actual is None:
                return False

            if actual is not self.BORRADO and actual.codigo == codigo:
                self.tabla[indice] = self.BORRADO
                self.elementos -= 1
                self.borrados += 1
                return True

        return False

    def factor_carga(self):
        return self.elementos / self.capacidad

    def factor_ocupacion(self):
        """Incluye celdas activas y marcas BORRADO."""
        return (self.elementos + self.borrados) / self.capacidad

    def umbral_factor_carga(self):
        return self.UMBRAL_FACTOR_CARGA

    @staticmethod
    def es_primo(numero):
        if numero < 2:
            return False
        if numero % 2 == 0:
            return numero == 2
        divisor = 3
        while divisor * divisor <= numero:
            if numero % divisor == 0:
                return False
            divisor += 2
        return True

    @classmethod
    def siguiente_primo(cls, numero):
        candidato = max(2, numero)
        while not cls.es_primo(candidato):
            candidato += 1
        return candidato

    def _insertar_durante_rehash(self, estacion):
        indice, existente = self._localizar_para_insertar(
            estacion.codigo,
            durante_rehash=True
        )

        if existente is not None:
            raise RuntimeError(
                f"Codigo duplicado durante rehash: {estacion.codigo}"
            )

        if indice is None:
            raise RuntimeError(
                f"No se pudo reinsertar la estacion {estacion.codigo}."
            )

        self.tabla[indice] = estacion
        self.elementos += 1

    def rehash(self):
        """Duplica la capacidad al siguiente primo y conserva todos los elementos."""
        inicio = perf_counter_ns()

        tabla_anterior = self.tabla
        capacidad_anterior = self.capacidad
        elementos_anteriores = self.elementos
        borrados_anteriores = self.borrados
        sondeos_rehash_anteriores = self.sondeos_rehash
        colisiones_rehash_anteriores = self.colisiones_rehash

        elementos_a_reinsertar = [
            elemento
            for elemento in tabla_anterior
            if elemento is not None and elemento is not self.BORRADO
        ]

        try:
            nueva_capacidad = self.siguiente_primo(capacidad_anterior * 2)
            self.capacidad = nueva_capacidad
            self.tabla = [None] * nueva_capacidad
            self.elementos = 0
            self.borrados = 0

            for elemento in elementos_a_reinsertar:
                self._insertar_durante_rehash(elemento)

            if self.elementos != len(elementos_a_reinsertar):
                raise RuntimeError(
                    "El rehash no conservó la cantidad original de estaciones."
                )

        except Exception:
            # Ante cualquier fallo, se restaura la tabla anterior completa.
            self.tabla = tabla_anterior
            self.capacidad = capacidad_anterior
            self.elementos = elementos_anteriores
            self.borrados = borrados_anteriores
            self.sondeos_rehash = sondeos_rehash_anteriores
            self.colisiones_rehash = colisiones_rehash_anteriores
            raise

        else:
            self.rehashes += 1

        finally:
            self.tiempo_rehash_ns += perf_counter_ns() - inicio

    def mostrar(self):
        for indice, elemento in enumerate(self.tabla):
            if elemento is self.BORRADO:
                print(indice, "-> BORRADO")
            else:
                print(indice, "->", elemento)

    def mostrar_estadisticas(self):
        print("Elementos activos       :", self.elementos)
        print("Celdas borradas         :", self.borrados)
        print("Capacidad               :", self.capacidad)
        print("Factor de carga         :", f"{self.factor_carga():.4f}")
        print("Factor de ocupacion     :", f"{self.factor_ocupacion():.4f}")
        print("Umbral comun            :", self.umbral_factor_carga())
        print("Colisiones insercion    :", self.colisiones_insercion)
        print("Sondeos insercion       :", self.sondeos_insercion)
        print("Colisiones rehash       :", self.colisiones_rehash)
        print("Sondeos rehash          :", self.sondeos_rehash)
        print("Sondeos busqueda        :", self.sondeos_busqueda)
        print("Sondeos eliminacion     :", self.sondeos_eliminacion)
        print("Rehashings              :", self.rehashes)
        print("Tiempo acumulado rehash :", f"{self.tiempo_rehash_ns / 1_000_000:.3f} ms")
