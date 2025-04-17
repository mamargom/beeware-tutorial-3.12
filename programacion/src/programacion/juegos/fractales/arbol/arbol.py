from toga import Canvas

import asyncio

from math import radians, sin, cos
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

    NUM_ALTURAS = 6

    def __init__(self):
        self.rama_centro = None
        self.rama_derecha = None
        self.rama_izquierda = None



class Rama(Arbol):

    HACIA_ARRIBA =  -90
    HACIA_ABAJO  =   90
    HACIA_DCHA   =  -45
    HACIA_IZQA   =   45

    LONG_MAX     =  100

    def __init__(self, direccion, posicion, nivel):
        self.hoja = None
        self.direccion = direccion
        self.nivel = nivel
        
        self.posicion_inicio = posicion
        self.posicion_final = self.calcula_destino_del_tronco(posicion, direccion, self.nivel)

        self.color = "BROWN"
        self.grosor = 10

    def calcula_destino_del_tronco(self, posic_inicio:Posicion, direccion, nivel):
            angulo_rad = radians(direccion)
            coseno = cos(angulo_rad)
            seno = sin (angulo_rad)
            long = self.calcula_longitud(nivel)
            x_dest = posic_inicio.posicion_x + long * coseno
            y_dest = posic_inicio.posicion_y + long * seno  # Positivo hacia abajo en canvas
            return Posicion(x_dest, y_dest)
    
    def calcula_longitud(self, nivel):
        longitud = Rama.LONG_MAX - (Arbol.NUM_ALTURAS - nivel) * 5
        return longitud


    def pintate(self, canvas: Canvas):

        with canvas.Stroke(color=self.color, line_width=self.grosor) as s:
            s.move_to(*self.posicion_inicio.tupla())
            s.line_to(*self.posicion_final.tupla())      
        canvas.redraw()


class Hoja:
    def __init__(self, posicion):
        self.posicion = posicion
        self.grosor = 10
        self.color = "GREEN"

    def pintate(self, canvas: Canvas):
        with canvas.Fill(color='GREEN') as fill:
            fill.arc(self.posicion.posicion_x, self.posicion.posicion_y,self.grosor )
        canvas.redraw()

