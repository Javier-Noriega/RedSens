class Nodo:
    __slots__ = ("dato", "izq", "der", "h")
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None
        self.h = 1            # altura almacenada (solo la usa el AVL)


class ArbolBusqueda:
    """Base común de ABB y AVL: búsqueda, recorridos, métodos recursivos
    (altura, nodos, hojas), consulta por rango y reporte de críticas.
    Convención: altura de árbol vacío = 0, una hoja = 1."""
    def __init__(self):
        self.raiz = None
    def insertar(self, e):            # devuelve False si el número ya existe
        raise NotImplementedError
    def eliminar(self, numero):       # devuelve False si no existe
        raise NotImplementedError
    def buscar(self, numero):
        """Búsqueda iterativa por número."""
        actual = self.raiz
        while actual is not None:
            k = actual.dato.numero
            if numero == k:
                return actual.dato
            actual = actual.izq if numero < k else actual.der
        return None
    # ---------- Métodos recursivos ----------
    def altura(self):
        return self._altura(self.raiz)
    def _altura(self, n):
        if n is None:                                  # CASO BASE
            return 0
        return 1 + max(self._altura(n.izq), self._altura(n.der))
    def altura_iterativa(self):
        """Altura sin recursión (recorre por niveles con listas). Sirve para árboles
        degenerados, donde la versión recursiva excede el límite de recursión de Python."""
        if self.raiz is None:
            return 0
        nivel = [self.raiz]
        h = 0
        while nivel:
            h += 1
            siguiente = []
            for n in nivel:
                if n.izq is not None:
                    siguiente.append(n.izq)
                if n.der is not None:
                    siguiente.append(n.der)
            nivel = siguiente
        return h
    def cantidad_nodos(self):
        return self._cantidad_nodos(self.raiz)
    def _cantidad_nodos(self, n):
        if n is None:                                  # CASO BASE
            return 0
        return 1 + self._cantidad_nodos(n.izq) + self._cantidad_nodos(n.der)
    def cantidad_hojas(self):
        return self._cantidad_hojas(self.raiz)
    def _cantidad_hojas(self, n):
        if n is None:                                  # CASO BASE 1
            return 0
        if n.izq is None and n.der is None:            # CASO BASE 2: hoja
            return 1
        return self._cantidad_hojas(n.izq) + self._cantidad_hojas(n.der)
    # ---------- Recorridos ----------
    def inorden(self):
        out = []
        self._inorden(self.raiz, out)
        return out
    def _inorden(self, n, out):
        if n is None:
            return
        self._inorden(n.izq, out)
        out.append(n.dato)
        self._inorden(n.der, out)
    def preorden(self):
        out = []
        self._preorden(self.raiz, out)
        return out
    def _preorden(self, n, out):
        if n is None:
            return
        out.append(n.dato)
        self._preorden(n.izq, out)
        self._preorden(n.der, out)
    def postorden(self):
        out = []
        self._postorden(self.raiz, out)
        return out
    def _postorden(self, n, out):
        if n is None:
            return
        self._postorden(n.izq, out)
        self._postorden(n.der, out)
        out.append(n.dato)
    # ---------- Consultas ----------
    def rango(self, a, b):
        """Estaciones con número entre a y b (inclusive), en orden. Poda ramas fuera de rango."""
        out = []
        self._rango(self.raiz, a, b, out)
        return out
    def _rango(self, n, a, b, out):
        if n is None:
            return
        k = n.dato.numero
        if a < k:
            self._rango(n.izq, a, b, out)
        if a <= k <= b:
            out.append(n.dato)
        if k < b:
            self._rango(n.der, a, b, out)
    def criticas(self):
        """Estaciones con batería < 20 ordenadas por número (inorden filtrado). Alimenta al M3."""
        out = []
        self._criticas(self.raiz, out)
        return out
    def _criticas(self, n, out):
        if n is None:
            return
        self._criticas(n.izq, out)
        if n.dato.bateria < 20:
            out.append(n.dato)
        self._criticas(n.der, out)