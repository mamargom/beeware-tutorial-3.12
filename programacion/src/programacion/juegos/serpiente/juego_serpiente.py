import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
import asyncio

from .helpers.serpiente import Serpiente, Cabeza

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20



class JuegoSerpiente(toga.App):

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

        self.serpiente = Serpiente(5)

        self.direction = "RIGHT"
        self.running = True

        self.cnt = 1;

        self.canvas = toga.Canvas(style=Pack(flex=1, background_color="white"))
        self.status_label = toga.Label("Playing...", style=Pack(padding=5))

        btn_up = toga.Button("↑", on_press=self.move_up, style=Pack(width=40, height=40))
        btn_down = toga.Button("↓", on_press=self.move_down, style=Pack(width=40, height=40))
        btn_left = toga.Button("←", on_press=self.move_left, style=Pack(width=40, height=40))
        btn_right = toga.Button("→", on_press=self.move_right, style=Pack(width=40, height=40))
        btn_restart = toga.Button("Restart", on_press=self.restart_game, style=Pack(width=80, height=40))

        controls = toga.Box(style=Pack(direction=ROW))
        controls.add(btn_left)
        controls.add(btn_up)
        controls.add(btn_down)
        controls.add(btn_right)
        controls.add(btn_restart)

        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_box.add(self.canvas)
        self.main_box.add(self.status_label)
        self.main_box.add(controls)

        asyncio.get_event_loop().create_task(self.game_loop())

    async def game_loop(self):
        while True:
            await asyncio.sleep(0.5)
            if self.running:
                self.cnt += 1;
                print("game loop - entry" + str(self.cnt))
                self.update_game()
                print("game loop - out" + str(self.cnt))


    def draw_game(self, canvas, context):
        self.serpiente.pintate(canvas)
        self.canvas.redraw()
        

    def update_game(self):
        if not self.running:
            return

        self.canvas.redraw()
        self.serpiente.borrate(self.canvas)
        self.canvas.redraw()

        if self.direction == "UP":
            self.serpiente.mueve_arriba()
        elif self.direction == "DOWN":
            self.serpiente.mueve_abajo()
        elif self.direction == "LEFT":
            self.serpiente.mueve_a_izquierda()
        elif self.direction == "RIGHT":
            self.serpiente.mueve_a_derecha()

        self.draw_game(self.canvas, self.canvas.context)

    def restart_game(self, widget):
        self.running = False
        self.direction = "RIGHT"
        self.status_label.text = "Stopped..."
        #self.canvas.redraw()
        self.serpiente.borrate(self.canvas)
        self.serpiente = Serpiente(5)
        self.draw_game(self.canvas, self.canvas.context)
        self.running = True
        self.status_label.text = "Playing..."

    def stop_game(self):
        self.running = False

    def move_up(self, widget):
        if self.direction != "DOWN":
            self.direction = "UP"
    
    def move_down(self, widget):
        if self.direction != "UP":
            self.direction = "DOWN"
    
    def move_left(self, widget):
        if self.direction != "RIGHT":
            self.direction = "LEFT"
    
    def move_right(self, widget):
        if self.direction != "LEFT":
            self.direction = "RIGHT"

def crea_box_de_juego():
    return JuegoSerpiente.obtenerInstanciaSingleton().main_box