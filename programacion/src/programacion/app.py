import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.window import Window, WindowSet
import importlib

from programacion.juegos.serpiente import juego_serpiente, gpt_juego_serpiente
from programacion.juegos.reflejos import juego_reflejos 
from programacion.juegos.fractales.arbol import juego_arbol

class GameSelector(toga.App):
    def startup(self):

        self.main_window = Window("elige un juego")
        self.selection_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.running = False
        
        self.juegos = {
            #"Serpiente": "helloworld.juegos.serpiente.juego_serpiente",  # Nombre del módulo Python
            "Serpiente": lambda : juego_serpiente.crea_box_de_juego(),
            "Arbol"    : lambda : juego_arbol.crea_box_de_juego(),
            "Reflejos" : lambda : juego_reflejos.crea_box_de_juego(),  
        }
        
        for nombre_del_juego, box_de_juego in self.juegos.items():
            button = toga.Button(
                text=nombre_del_juego,
                on_press=lambda widget, box=box_de_juego: self.carga_un_juego(nombre_del_juego, box()),  
                style=Pack(padding=5)
            )
            self.selection_box.add(button)

        self.main_window.on_close = lambda widget: self.cierra_app()
        #carga el menu selector
        self.carga_un_juego("Elije juego", self.selection_box)


    def cierra_app(self):
        if self.main_window.content == self.selection_box:
            self.app.exit()
        else:
            #self.app.main_window.content.stop_game()
            self.carga_un_juego("elige un juego", self.selection_box)
        

    def carga_un_juego(self, titulo, box_de_juego):
        try:
            self.app.main_window.content = box_de_juego
            self.app.main_window.title = titulo
            self.app.main_window.show()
        except Exception as e:
            print(f"Error al cargar el juego {box_de_juego}: {e}")

if __name__ == "__main__":
    GameSelector("Game Selector", "com.example.gameselector").main_loop()
