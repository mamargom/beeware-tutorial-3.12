
class Serpiente():

    _DIAMETRO_CABEZA = 30

    def __init__(self, longitud_serpiente, posicion_x=0, posicion_y=0):
        # cabeza 
        self.cabeza = Cabeza(posicion_x,posicion_y)

        # cuerpo
        if longitud_serpiente == 1:  self.cola = None # solo tiene cabeza
        else: self.cola = Serpiente(longitud_serpiente-1, 
                                    posicion_x+Serpiente._DIAMETRO_CABEZA, 
                                    posicion_y+Serpiente._DIAMETRO_CABEZA)

    def dame_cabeza(self):
        return self.cabeza
    def dame_cola(self):
        return self.cola
    
    def longitud(self):
            if self.cola == None: return 1
            else: return 1 + self.cola.longitud()   

class Cabeza():
        def __init__(self,posicion_x, posicion_y):
            self.mueve_a_posicion(posicion_x,posicion_y)
            self.diametro_cabeza = Serpiente._DIAMETRO_CABEZA;

        def mueve_a_posicion(self, x,y):
            self._posicion_x = x
            self._posicion_y = y

        def dime_posicion(self):
            return (self._posicion_x, self.posicion_y)            


        