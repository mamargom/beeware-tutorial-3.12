from toga import Canvas


from .helpers.support import *



class Posicion:
        def __init__(self, posicion_x=0, posicion_y=0):
            self.posicion_x = posicion_x
            self.posicion_y = posicion_y

        def tupla(self):
            return (self.posicion_x, self.posicion_y)


# un arbol puede tener 3 ramas 
# cada rama puede tener una hoja y/o sostener un arbol (con 3 ramas cada una)

class Arbol:

    # Posicion inicial
    POSICION_RAIZ = Posicion(0,0)

    # cada vez que re pinta el arbol se actualizan estos parametros
    ALTURAS = 6
    MAX_TAMANO = 1024
    DIMENSIONES = None
    
    COLOR = "BROWN"
    GROSOR = 10
    GROSOR_HOJA = 5

    CANVAS = None




class Rama(Arbol):

    HACIA_ARRIBA =  -90
    HACIA_ABAJO  =   90
    HACIA_DCHA   =  -45
    HACIA_IZQA   =   45

    LONG_MAX     =  100
    MAX_GROSOR   =   80


class Hoja:
    COLOR = "GREEN"


