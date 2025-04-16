import toga
from toga import Canvas
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from math import radians, cos, sin


class JuegoRecursionArbol(toga.App):

    
    DERECHA   = 45  #grados
    IZQUIERDA = 135 #grados
    ARRIBA    = 90   #grados


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

        self.x_inicio = 0
        self.y_inicio = 0

        self.running = True
        self.canvas = toga.Canvas(style=Pack(flex=1, background_color="white"))
        self.canvas.on_resize = self.cambiar_punto_inicio
        self.status_label = toga.Label("Jugando...", style=Pack(padding=5))

        btn_restart = toga.Button("Restart", on_press=self.restart_game, style=Pack(width=80, height=40))

        controls = toga.Box(style=Pack(direction=ROW))
        controls.add(btn_restart)


        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_box.add(self.canvas)
        self.main_box.add(self.status_label)
        self.main_box.add(controls)

        self.canvas.redraw()

    def restart_game(self, widget):
        self.pinta_linea_simple(self.x_inicio, self.y_inicio, self.ARRIBA, 100)
        self.pinta_linea_simple(self.x_inicio, self.y_inicio, self.DERECHA, 100)
        self.pinta_linea_simple(self.x_inicio, self.y_inicio, self.IZQUIERDA, 100)

        self.canvas.redraw()


    ################################
    # métodos para pintar el árbol #
    ################################

    def punto_destino_del_arbol(self, x, y, angulo_grados, distancia):

        angulo_rad = radians(angulo_grados)
        x_dest = x + distancia * cos(angulo_rad)
        y_dest = y + distancia * sin(angulo_rad)  # Positivo hacia abajo en canvas
        return x_dest, y_dest

    def punto_inicial(self):
        self.canvas.on_resize

    def cambiar_punto_inicio(self, canvas, width, height):
        print(f"Tamaño del canvas: {width}x{height}")

        # Punto de inicio: centro del borde inferior
        self.x_inicio = width / 2
        self.y_inicio = height

    def pinta_linea_simple(self, x_inicio, y_inicio, angulo, longitud):
        # Punto destino: hacia arriba en ángulo 135° (45° arriba a la izquierda)
        angulo_rad = radians(angulo)
        x_fin = x_inicio + longitud * cos(angulo_rad)
        y_fin = y_inicio - longitud * sin(angulo_rad)

        with self.canvas.Stroke('blue', line_width=5) as s:
            s.move_to(x_inicio, y_inicio)
            s.line_to(x_fin, y_fin)


def crea_box_de_juego():
    return JuegoRecursionArbol.obtenerInstanciaSingleton().main_box