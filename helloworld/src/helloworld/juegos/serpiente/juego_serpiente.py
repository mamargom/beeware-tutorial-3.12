import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import random
import asyncio
from .helpers.serpiente import Serpiente, Cabeza

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20

class SnakeGame:
    def __init__(self):
        self.serpiente = Serpiente(5)
        self.direction = "RIGHT"
        self.running = True
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.random_food()

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
                self.update_game()

    def draw_game(self):
        with self.canvas.context.Fill(color="red") as fill:
            for x, y in self.snake:
                fill.rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.canvas.redraw()

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
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1
        elif self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
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

        self.draw_game()

    def restart_game(self, widget):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.random_food()
        self.direction = "RIGHT"
        self.running = True
        self.status_label.text = "Playing..."
        self.draw_game()

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

def create_game():
    return SnakeGame().main_box
