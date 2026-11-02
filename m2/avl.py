from .arbol_busqueda import ArbolBusqueda, Nodo


class AVL(ArbolBusqueda):
    """AVL: ABB que mantiene |factor de equilibrio| <= 1 con rotaciones."""
    def __init__(self):
        super().__init__()
        self._ok = False          # para informar si insertó / eliminó
    @staticmethod
    def _h(n):
        return 0 if n is None else n.h
    def _actualizar(self, n):
        n.h = 1 + max(self._h(n.izq), self._h(n.der))
    def _factor(self, n):
        """Factor de equilibrio = altura(izq) - altura(der)."""
        return 0 if n is None else self._h(n.izq) - self._h(n.der)
    def _rotar_derecha(self, y):
        """Rotación simple a la derecha (caso izquierda-izquierda)."""
        x = y.izq
        y.izq = x.der
        x.der = y
        self._actualizar(y)
        self._actualizar(x)
        return x
    def _rotar_izquierda(self, x):
        """Rotación simple a la izquierda (caso derecha-derecha)."""
        y = x.der
        x.der = y.izq
        y.izq = x
        self._actualizar(x)
        self._actualizar(y)
        return y
    def _balancear(self, n):
        """Actualiza altura, calcula el factor y aplica la rotación que corresponda."""
        self._actualizar(n)
        f = self._factor(n)
        if f > 1:                                       # pesado a la izquierda
            if self._factor(n.izq) < 0:                 # izquierda-derecha -> rotación doble
                n.izq = self._rotar_izquierda(n.izq)
            return self._rotar_derecha(n)
        if f < -1:                                      # pesado a la derecha
            if self._factor(n.der) > 0:                 # derecha-izquierda -> rotación doble
                n.der = self._rotar_derecha(n.der)
            return self._rotar_izquierda(n)
        return n
    def insertar(self, e):
        self._ok = False
        self.raiz = self._insertar(self.raiz, e)
        return self._ok
    def _insertar(self, n, e):
        if n is None:
            self._ok = True
            return Nodo(e)
        k, c = e.numero, n.dato.numero
        if k < c:
            n.izq = self._insertar(n.izq, e)
        elif k > c:
            n.der = self._insertar(n.der, e)
        else:
            return n                                    # repetida
        return self._balancear(n)
    def eliminar(self, numero):
        self._ok = False
        self.raiz = self._eliminar(self.raiz, numero)
        return self._ok
    def _eliminar(self, n, k):
        if n is None:
            return None
        c = n.dato.numero
        if k < c:
            n.izq = self._eliminar(n.izq, k)
        elif k > c:
            n.der = self._eliminar(n.der, k)
        else:
            self._ok = True
            if n.izq is None:
                return n.der
            if n.der is None:
                return n.izq
            sucesor = n.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            n.dato = sucesor.dato
            n.der = self._eliminar(n.der, sucesor.dato.numero)
        return self._balancear(n)                       # reequilibra al volver