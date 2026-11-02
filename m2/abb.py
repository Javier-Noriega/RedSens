from .arbol_busqueda import ArbolBusqueda, Nodo


class ABB(ArbolBusqueda):
    """Árbol binario de búsqueda sin balanceo."""
    def insertar(self, e):
        """Inserción iterativa: evita RecursionError si el árbol se degenera
        (claves ordenadas)."""
        nuevo = Nodo(e)
        if self.raiz is None:
            self.raiz = nuevo
            return True
        actual = self.raiz
        k = e.numero
        while True:
            c = actual.dato.numero
            if k == c:
                return False                      # clave repetida
            if k < c:
                if actual.izq is None:
                    actual.izq = nuevo
                    return True
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    return True
                actual = actual.der
    def eliminar(self, numero):
        if self.buscar(numero) is None:
            return False
        self.raiz = self._eliminar(self.raiz, numero)
        return True
    def _eliminar(self, n, k):
        if n is None:
            return None
        c = n.dato.numero
        if k < c:
            n.izq = self._eliminar(n.izq, k)
        elif k > c:
            n.der = self._eliminar(n.der, k)
        else:
            # Caso 1 (hoja) y caso 2 (un hijo): se reemplaza por el hijo que exista (o None)
            if n.izq is None:
                return n.der
            if n.der is None:
                return n.izq
            # Caso 3: dos hijos -> sucesor inorden (mínimo del subárbol derecho)
            sucesor = n.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            n.dato = sucesor.dato
            n.der = self._eliminar(n.der, sucesor.dato.numero)
        return n