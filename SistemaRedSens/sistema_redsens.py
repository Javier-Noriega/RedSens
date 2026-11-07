from hash.tabla_hash import Tablahash
from m2.abb import ABB
from m2.avl import AVL

class SistemaRedSens:

    def __init__(self):
        self.tabla_hash = Tablahash(11, "cuadratica")
        self.abb=ABB()
        self.avl=AVL()
        
