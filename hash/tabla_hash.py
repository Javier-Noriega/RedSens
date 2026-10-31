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

    
    def funcionhash(self,codigo):
        numero=int(codigo.split("-")[1])
        return numero % self.capacidad

    def insertar(self, estacion):
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
            print(i, "->", self.tabla[i])


    def mostrar_estadisticas(self):

        print("Elementos :", self.elementos)
        print("Colisiones:", self.colisiones)
        print("Sondeos   :", self.sondeos)

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

            if self.tabla[indice].codigo == codigo:
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

    