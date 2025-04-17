from toga import Canvas

class Figura:
    

    def __init__(self):
        self.posicion = (100,100)
        self.diametro = 50

    def mueve_a(self, posicion):
        self.posicion=posicion

    def cambia_diametro (self, diametro):
        self.diametro = diametro

    def pintate(self, canvas: Canvas, color="red"):
        with canvas.context.Fill(color=color) as fill:
            fill.arc(*self.posicion, self.diametro)

    def borrate(self, canvas):
        self.pintate(self, canvas, color="blanco")