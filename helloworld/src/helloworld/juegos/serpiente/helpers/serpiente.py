
class Serpiente():

    _DIAMETRO_CABEZA = 10

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

    def mueve_a_posicion(self, posicion_x, posicion_y):
        if self.cola == None:
            self.cabeza.mueve_a_posicion(posicion_x,posicion_y)
        else:
            posicion_cabeza = self.cabeza.dime_posicion()
            self.cabeza.mueve_a_posicion(posicion_x,posicion_y)
            self.cola.mueve_a_posicion(*posicion_cabeza)
        
    def mueve_a_derecha(self):
        self.mueve_a_posicion(self.cabeza._posicion_x + Serpiente._DIAMETRO_CABEZA, self.cabeza._posicion_y)
    def mueve_a_izquierda(self):
        self.mueve_a_posicion(self.cabeza._posicion_x - Serpiente._DIAMETRO_CABEZA, self.cabeza._posicion_y)
    def mueve_arriba(self):
        self.mueve_a_posicion(self.cabeza._posicion_x, self.cabeza._posicion_y - Serpiente._DIAMETRO_CABEZA)
    def mueve_abajo(self):
        self.mueve_a_posicion(self.cabeza._posicion_x, self.cabeza._posicion_y + Serpiente._DIAMETRO_CABEZA)

    def pintate(self, canvas):
        self.cabeza.pintate(canvas)
        if self.cola != None:
            self.cola.pintate(canvas)

class Cabeza():
        def __init__(self,posicion_x, posicion_y):
            self.mueve_a_posicion(posicion_x,posicion_y)
            self.diametro_cabeza = Serpiente._DIAMETRO_CABEZA;

        def mueve_a_posicion(self, x, y):
            self._posicion_x = x
            self._posicion_y = y

        def dime_posicion(self):
            return (self._posicion_x, self._posicion_y)

        def pintate(self, canvas):
            with canvas.context.Fill(color="red") as fill:
                fill.arc(self._posicion_x, self._posicion_y, self.diametro_cabeza)          


        