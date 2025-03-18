import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import importlib

from juegos.serpiente import juego_serpiente

class GameSelector(toga.App):
    def startup(self):

        self.main_window = toga.MainWindow(title=self.formal_name)
        
        self.games = {
            #"Serpiente": "helloworld.juegos.serpiente.juego_serpiente",  # Nombre del módulo Python
            "Serpiente": juego_serpiente.__name__,
            "Juego 2": "juego2",  
            "Juego 3": "juego3"   
        }

        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        for game_name, game_module in self.games.items():
            button = toga.Button(
                text=game_name,
                on_press=lambda widget, module=game_module:self.load_game(module),
                style=Pack(padding=5)
            )
            self.main_box.add(button)
        
        self.main_window.content = self.main_box
        self.main_window.show()

    def load_game(self, module_name):
        try:
            #game_module = importlib.import_module(module_name)
            #game_widget = game_module.create_game()
            #self.main_window.content = game_widget
            self.main_window.content = juego_serpiente.create_game()
        except Exception as e:
            print(f"Error al cargar el juego {module_name}: {e}")

if __name__ == "__main__":
    GameSelector("Game Selector", "com.example.gameselector").main_loop()
