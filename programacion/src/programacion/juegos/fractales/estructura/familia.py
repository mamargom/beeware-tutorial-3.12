# Familia será triangulo para abajo.
# (Padre/Madre) será triangulo hacia arriba en medio
# deja espacio para 3 familias (3 triangulos hacia abajo).  
# Y Así recursivamente

class Familia:

    def __init__(self):
        self.padre = Padre()
        self.madre = Madre()
        self.hijo1 = None
        self.hijo2 = None
        self.hijo3 = None

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pareja = None
        self.familia = Familia()
        

class Padre(Persona):
    def __init__(self):
        pass

class Madre(Persona):
    def __init__(self):
        pass

class Hijo(Persona):
    def __init__(self, padre, madre):
        self.padre = padre
        self.madre = madre