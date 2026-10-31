class estacion:
    def __init__(
        self,
        codigo,
        numero,
        nombre,
        localidad,
        tipo,
        bateria,
        diasSinVisita
    ):
        self.codigo=codigo
        self.numero=numero
        self.nombre=nombre
        self.localidad=localidad
        self.tipo=tipo
        self.bateria=bateria
        self.diasSinVisita=diasSinVisita

    def __str__(self):
        return f"{self.nombre} - {self.numero}"
        