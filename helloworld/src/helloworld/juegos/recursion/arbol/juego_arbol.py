import toga
from toga import Canvas
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from math import log10

from .helpers.support import *


import asyncio



class JuegoRecursionArbol(toga.App):

    MAX_NUM_ALTURAS = 8
    MAX_GROSOR = 100

    TIEMPO_ESPERA = 0.001

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
        
        asyncio.get_event_loop().create_task(
            self.recorre_arbol(self.x_inicio, self.y_inicio, -90, JuegoRecursionArbol.MAX_GROSOR, 0))
        self.canvas.redraw()


    ################################
    # métodos para pintar el árbol #
    ################################

    def cambiar_punto_inicio(self, canvas, width, height):
        print(f"Tamaño del canvas: {width}x{height}")
        

        # Punto de inicio: centro del borde inferior
        self.x_inicio = width / 2
        self.y_inicio = height


    async def recorre_arbol(self, x_inicio, y_inicio, angulo, longitud, numero_de_alturas):

        #print(f"recorre_arbol: nivel:{numero_de_alturas} long{longitud}: ang {angulo}")
        #print(f"       posic1:{x_inicio},{y_inicio} posic2{destino_del_tronco(x_inicio, y_inicio, angulo, longitud)}")
        await asyncio.sleep(JuegoRecursionArbol.TIEMPO_ESPERA)
        self.canvas.window.content.refresh()

        if (numero_de_alturas == JuegoRecursionArbol.MAX_NUM_ALTURAS):
            self.pinta_hoja(x_inicio, y_inicio)
        elif (numero_de_alturas < JuegoRecursionArbol.MAX_NUM_ALTURAS / 3):
            x,y = self.pinta_tronco(x_inicio, y_inicio, angulo, longitud, numero_de_alturas) 
            await self.recorre_arbol(x, y, angulo, longitud-10, numero_de_alturas+1)
        else:
            # recto
            x,y = self.pinta_tronco(x_inicio, y_inicio, angulo, longitud, numero_de_alturas) 
            await self.recorre_arbol(x, y, angulo, longitud-10, numero_de_alturas+1)
            # dcha
            x,y = self.pinta_tronco(x_inicio, y_inicio, rotar_derecha(angulo), longitud, numero_de_alturas) 
            await self.recorre_arbol(x, y, rotar_derecha(angulo), longitud-10, numero_de_alturas+1)
            # dcha
            x,y = self.pinta_tronco(x_inicio, y_inicio, rotar_izquierda(angulo), longitud, numero_de_alturas) 
            await self.recorre_arbol(x, y, rotar_izquierda(angulo), longitud-10, numero_de_alturas+1)
        
        
    def pinta_tronco(self, x_inicio, y_inicio, angulo, longitud, nivel):

        x_fin, y_fin = destino_del_tronco(x_inicio, y_inicio, angulo, longitud)
        with self.canvas.Stroke('blue', line_width=reduce_grosor(nivel, JuegoRecursionArbol.MAX_GROSOR)) as s:
            s.move_to(x_inicio, y_inicio)
            s.line_to(x_fin, y_fin)
        
        self.canvas.redraw()
        return x_fin, y_fin 
    

    def pinta_hoja(self, x_inicio, y_inicio):

        with self.canvas.fill(color='GREEN') as fill:
            fill.arc(x_inicio, y_inicio, 5)

        self.canvas.redraw()



def crea_box_de_juego():
    return JuegoRecursionArbol.obtenerInstanciaSingleton().main_box