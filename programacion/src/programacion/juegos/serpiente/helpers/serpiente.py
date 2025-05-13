
from toga import Canvas

class Serpiente():

    _DIAMETRO_CABEZA = 10

    def __init__(self, longitud_serpiente, posicion_x=0, posicion_y=0):
        
        #mirar el caso si longitud <= 0
        
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
        self.mueve_a_posicion(*self.cabeza.posic_dcha())
    def mueve_a_izquierda(self):
        self.mueve_a_posicion(*self.cabeza.posic_izqa())
    def mueve_arriba(self):
        self.mueve_a_posicion(*self.cabeza.posic_arriba())
    def mueve_abajo(self):
        self.mueve_a_posicion(*self.cabeza.posic_abajo())

    def pintate(self, canvas, color="red"):
        self.cabeza.pintate(canvas, color)
        if self.cola != None:
            self.cola.pintate(canvas, color)

    def borrate(self, canvas: Canvas):
        self.pintate(canvas, "white")

class Cabeza():
        def __init__(self,posicion_x, posicion_y):
            self.mueve_a_posicion(posicion_x,posicion_y)
            self.diametro_cabeza = Serpiente._DIAMETRO_CABEZA;

        def mueve_a_dcha(self):
            self.mueve_a_posicion(*self.posic_dcha())

        def posic_dcha(self):
            posicion_actual = self.dime_posicion()
            return (posicion_actual[0] + self.diametro_cabeza, posicion_actual[1])
        
        def mueve_a_izqa(self):
            self.mueve_a_posicion(*self.posic_izqa())

        def posic_izqa(self):
            posicion_actual = self.dime_posicion()
            return (posicion_actual[0] - self.diametro_cabeza, posicion_actual[1])        

        def mueve_arriba(self):
            self.mueve_a_posicion(*self.posic_arriba())

        def posic_arriba(self):
            posicion_actual = self.dime_posicion()
            return (posicion_actual[0], posicion_actual[1] - self.diametro_cabeza)        

        def mueve_abajo(self):
            self.mueve_a_posicion(*self.posic_abajo())

        def posic_abajo(self):
            posicion_actual = self.dime_posicion()
            return (posicion_actual[0], posicion_actual[1] + self.diametro_cabeza)  

        def mueve_a_posicion(self, x, y):
            self._posicion_x = x
            self._posicion_y = y

        def dime_posicion(self):
            return (self._posicion_x, self._posicion_y)

        def pintate(self, canvas:Canvas, color):
            with canvas.context.Fill(color=color) as fill:
                fill.arc(self._posicion_x, self._posicion_y, self.diametro_cabeza)          


        