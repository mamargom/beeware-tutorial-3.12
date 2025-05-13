import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .figura import Figura




class JuegoReflejos(toga.App):

    _instancia = None
    _permitir_instanciacion = False

    def __new__(cls, *args, **kwargs):
        if not cls._permitir_instanciacion:
            raise Exception("Usa 'obtenerInstanciaSingleton()' para obtener la instancia.")
        return super().__new__(cls)

    @classmethod
    def obtenerInstanciaSingleton(cls):
        if cls._instancia is None:
            cls._permitir_instanciacion = True
            cls._instancia = cls()
            cls._permitir_instanciacion = False
        return cls._instancia

    
    def __init__(self):

        self.running = True

        self.canvas = toga.Canvas(style=Pack(flex=1, background_color="white"), on_press=self.provide_coordinates)

        self.status_label = toga.Label("Preparado...", style=Pack(padding=5))
        
        self.label_coordenadas = toga.Label("coordenadas: ")
        self.text_coordenadas = toga.Label("(x,y)")
        btn_restart = toga.Button("Restart", on_press=self.restart_game, style=Pack(width=80, height=40))

        controls = toga.Box(style=Pack(direction=ROW))
        controls.add(btn_restart)
        controls.add(self.label_coordenadas)
        controls.add(self.text_coordenadas)

        # Imagen
        self.figura = Figura()

        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_box.add(self.canvas)
        self.main_box.add(controls)

        self.canvas.redraw()


    def restart_game(self, widget):
        self.figura.pintate(self.canvas)
        self.canvas.redraw()
    
    def provide_coordinates(self, widget, x, y):
        self.text_coordenadas.text = f"({x}, {y}) -> {self.figura.punto_en_circulo((x,y))}"
        self.canvas.redraw()

def crea_box_de_juego():
    return JuegoReflejos.obtenerInstanciaSingleton().main_box