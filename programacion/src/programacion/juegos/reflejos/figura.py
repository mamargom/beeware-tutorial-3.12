from toga import Canvas

class Figura:
    
    def __init__(self):
        self.posicion = (100,100)
        self.radio = 50

    def mueve_a(self, posicion):
        self.posicion=posicion

    def cambia_diametro (self, radio):
        self.radio = radio

    def pintate(self, canvas: Canvas, color="red"):
        with canvas.context.Fill(color=color) as fill:
            fill.arc(*self.posicion, self.radio)

    def borrate(self, canvas):
        self.pintate(self, canvas, color="blanco")

    def punto_en_circulo(self, punto):
        a, b = punto
        x, y = self.posicion
        r = self.radio
        return (a - x)**2 + (b - y)**2 <= r**2

