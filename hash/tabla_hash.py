class Tablahash:
    SONDEO_LINEAL = "lineal"
    SONDEO_CUADRATICA = "cuadratica"
    BORRADO = object()
    
    def __init__(self,capacidad,SONDEO):
        self.capacidad=capacidad
        self.tabla=[None] * capacidad
        self.elementos=0
        self.SONDEO=SONDEO
        self.colisiones = 0
        self.sondeos = 0
        self.rehashes = 0

    
    def funcionhash(self,codigo):
        numero=int(codigo.split("-")[1])
        return numero % self.capacidad

    def insertar(self, estacion):

        if self.factor_carga() >= self.umbral_factor_carga():
            self.rehash()      
            
        intento=1
        indice = self.funcionhash(estacion.codigo)
        self.sondeos += 1
        if self.tabla[indice] is None:
            self.tabla[indice] = estacion
            self.elementos += 1
        else:
            while(True):
                indicenuevocalculado=self.calcularindice(indice,intento)
                self.sondeos += 1
                if self.tabla[indicenuevocalculado] is None:
                    self.tabla[indicenuevocalculado]=estacion
                    self.elementos+=1
                    return
                self.colisiones+=1
                intento+=1
                

    def calcularindice(self,hashbase,intento):
        if self.SONDEO==self.SONDEO_LINEAL:
            return (hashbase + intento) % self.capacidad
        if self.SONDEO==self.SONDEO_CUADRATICA:
            return (hashbase + intento*intento) % self.capacidad

    def mostrar(self):

        for i in range(self.capacidad):

            if self.tabla[i] is self.BORRADO:
                print(i, "-> BORRADO")
            else:
                print(i, "->", self.tabla[i])

    def mostrar_estadisticas(self):

        print("Elementos     :", self.elementos)
        print("Capacidad     :", self.capacidad)
        print("Factor carga  :", self.factor_carga())
        print("Colisiones    :", self.colisiones)
        print("Sondeos       :", self.sondeos)
        print("Rehashings    :", self.rehashes)

    def buscar(self, codigo):

        hashbase = self.funcionhash(codigo)

        intento = 0

        while intento < self.capacidad:

            indice = self.calcularindice(
                hashbase,
                intento
            )

            if self.tabla[indice] is None:
                return None

            if (
                self.tabla[indice] != self.BORRADO
                and self.tabla[indice].codigo == codigo
            ):
                return self.tabla[indice]

            intento += 1

        return None

    def eliminar(self, codigo):
        hashbase = self.funcionhash(codigo)
        intento = 0
        while intento < self.capacidad:
            indice = self.calcularindice(hashbase,intento)
            if self.tabla[indice] is None:
                return False
            if (
                self.tabla[indice] != self.BORRADO
                and self.tabla[indice].codigo == codigo
            ):
                self.tabla[indice] = self.BORRADO
                self.elementos -= 1
                return True
            intento += 1
        return False

    def factor_carga(self):
        return self.elementos / self.capacidad

    def es_primo(self, numero):

        if numero < 2:
            return False

        for i in range(2, int(numero ** 0.5) + 1):

            if numero % i == 0:
                return False

        return True

    def siguiente_primo(self, numero):

        candidato = numero

        while not self.es_primo(candidato):
            candidato += 1

        return candidato

    def rehash(self):

        nueva_capacidad = self.siguiente_primo(
            self.capacidad * 2
        )

        tabla_vieja = self.tabla

        self.capacidad = nueva_capacidad

        self.tabla = [None] * nueva_capacidad

        self.elementos = 0

        self.rehashes += 1

        for elemento in tabla_vieja:

            if (
                elemento is not None
                and elemento != self.BORRADO
            ):
                self.insertar(elemento)

    def umbral_factor_carga(self):

        if self.SONDEO == self.SONDEO_LINEAL:
            return 0.70

        return 0.80