import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
import asyncio
import time

from juegos.serpiente.helpers.serpiente import Serpiente
from juegos.serpiente.helpers.serpiente import Cabeza

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20



class SnakeGame(toga.App):
    serpiente = Serpiente(5);
    
    def startup(self):
        long = SnakeGame.serpiente.longitud()

        self.main_window = toga.MainWindow(title=self.name)
        self.direction = "RIGHT"
        self.running = True

        self.cnt = 1;

        self.x_circ = 50;
        self.y_circ = 50;
        self.x_rect = 80;
        self.y_rect = 80;


        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.random_food()

        self.canvas = toga.Canvas(style=Pack(flex=1))
        self.canvas.redraw()

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

        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(self.canvas)
        main_box.add(self.status_label)
        main_box.add(controls)

        self.main_window.content = main_box
        self.main_window.show()

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

    def pinta_serpiente(self, serpiente: Serpiente):
        self.pinta_cabeza(serpiente.cabeza)
        if serpiente.cola != None: 
            self.pinta_serpiente(serpiente.cola)


    def draw_game(self, canvas, context):
        self.pinta_serpiente (SnakeGame.serpiente)
        
    def random_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def update_game(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "UP":
            print("UP")
            head_y -= 1
        elif self.direction == "DOWN":
            print("DOWN")
            head_y += 1
        elif self.direction == "LEFT":
            print("LEFT")
            head_x -= 1
        elif self.direction == "RIGHT":
            print("RIGHT")
            head_x += 1

        new_head = (head_x, head_y)

        if new_head in self.snake or not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT):
            self.running = False
            self.status_label.text = "Game Over! Press Restart"
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.random_food()
        else:
            self.snake.pop()

        self.draw_game(self.canvas, self.canvas.context)

    def restart_game(self, widget):
        self.snake = [(5, 5), (4, 5), (3, 5)]
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
