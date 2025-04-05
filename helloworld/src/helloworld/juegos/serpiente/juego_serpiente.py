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
    
    def __init__(self):

        self.serpiente = Serpiente(5)

        self.direction = "RIGHT"
        self.running = True

        self.cnt = 1;

        self.canvas = toga.Canvas(style=Pack(flex=1))
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
            await asyncio.sleep(0.2)
            if self.running:
                self.cnt += 1;
                print("game loop - entry" + str(self.cnt))
                self.update_game()
                print("game loop - out" + str(self.cnt))

    def pinta_cabeza(self, cabeza: Cabeza):
        with self.canvas.context.Fill(color="red") as fill:
            circle = fill.arc(cabeza._posicion_x, cabeza._posicion_y, cabeza.diametro_cabeza)
            self.canvas.redraw()

    def draw_game(self, canvas, context):
        self.serpiente.pintate(canvas)
        #self.comida.pintate(canvas)
        self.canvas.redraw()
        
    def random_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def update_game(self):
        if not self.running:
            return

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
        self.food = self.random_food()
        self.direction = "RIGHT"
        self.running = True
        self.status_label.text = "Playing..."
        #self.canvas.redraw()
        self.draw_game(self.canvas, self.canvas.context)

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
    return JuegoSerpiente().main_box