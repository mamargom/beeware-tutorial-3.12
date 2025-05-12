import toga
from toga import Canvas
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
import time

from .helpers.support import *
from .arbol import Arbol, Rama, Hoja, Posicion
 


class JuegoRecursionArbol(toga.App):


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
        
        self.velocidad = 0

        self.running = True
        

        btn_restart = toga.Button("Pinta ! ", on_press=self.restart_game, style=Pack(width=80, height=40))
        self.slider_velocidad = toga.Slider("velocidad", value=0, min=0, max=0.5, on_release=self.muestra_velocidad)
        self.pre_recursion = toga.Switch("pinta_antes", value = True)
        self.slider_r = toga.Slider("r", value=0.8, min=0.4, max=0.9, on_release=self.muestra_velocidad)
        self.slider_L0 = toga.Slider("L0", value=0.2, min=0.1, max=0.3, on_release=self.muestra_velocidad)
        self.slider_hoja_ratio = toga.Slider("slider_hoja_ratio", value=0.05, min=0, max=0.3, on_release=self.muestra_velocidad)
        controls = toga.Box(style=Pack(direction=ROW))
        controls.add(toga.Label("speed: "))
        controls.add(self.slider_velocidad)
        controls.add(toga.Label("r: "))
        controls.add(self.slider_r)
        controls.add(toga.Label("L0: "))
        controls.add(self.slider_L0)
        controls.add(toga.Label("Hoja: "))
        controls.add(self.slider_hoja_ratio)
        
        controls.add(self.pre_recursion)
        controls.add(btn_restart)


        self.canvas = toga.Canvas(style=Pack(flex=1, background_color="white"))
        self.canvas.on_resize = self.cambiar_punto_inicio
        self.status_label = toga.Label("Jugando...", style=Pack(padding=5))

        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_box.add(self.canvas)
        self.main_box.add(self.status_label)
        self.main_box.add(controls)

        self.arbol = None

        self.canvas.redraw()


    def muestra_velocidad(self, widget):
        self.status_label.text = widget.value
    
    def muestra_r(self, widget):
        self.status_label.text = widget.value


    def limpia_canvas(self):
        with self.canvas.Fill(color="WHITE") as fill:
            fill.rect(0,0,self.tamano_canvas[0],self.tamano_canvas[1])

    async def restart_game(self, widget):

        self.limpia_canvas()
    
        #inicia propiedades del árbol
        # r cambia ratio reduccion de grosor
        # L0 ratio de tamano tronco
        # hoja_ratio ratio tamano de hoja
        Arbol.MAX_TAMANO = self.tamano_canvas[1]
        Arbol.DIMENSIONES = calcula_dimensiones_de_nivel(Arbol.MAX_TAMANO, 
                                                        self.slider_r.value, #ok=0.8
                                                        self.slider_L0.value, #ok=0.3
                                                        self.slider_hoja_ratio.value, #ok=0.05
                                                        max_niveles=8) #ok=8
        Arbol.ALTURAS = len(Arbol.DIMENSIONES) - 1
        Arbol.CANVAS = self.canvas

        for (long,grosor) in Arbol.DIMENSIONES:
            print(f"Tamaño ramas: {long}x{grosor}")


        asyncio.get_event_loop().create_task(self.pinta_arbol(Arbol.POSICION_RAIZ, Rama.HACIA_ARRIBA, Arbol.ALTURAS))
#        pinta_arbol_sync (Arbol.POSICION_RAIZ, Rama.HACIA_ARRIBA, Arbol.ALTURAS)

        self.canvas.redraw()

        return


    # recorre usando la estructura
    async def pinta_arbol(self, posicion, direccion, altura):

        if self.slider_velocidad.value > 0:
            await asyncio.sleep(self.slider_velocidad.value)

        nueva_posicion = mueve_arbol(posicion, direccion, altura)

        if (self.pre_recursion.value):
            pinta_rama(posicion, direccion, altura)
        
        if (altura == 0):
            pinta_hoja(nueva_posicion)
        elif (altura > Arbol.ALTURAS - 1):
            await self.pinta_arbol(nueva_posicion, direccion, altura-1)
        else:
            await self.pinta_arbol(nueva_posicion, direccion, altura-1)
            await self.pinta_arbol(nueva_posicion, rotar_derecha(direccion), altura-1)
            await self.pinta_arbol(nueva_posicion, rotar_izquierda(direccion), altura-1)
        
        if (not self.pre_recursion.value):
            pinta_rama(posicion, direccion, altura)



    def cambiar_punto_inicio(self, canvas, width, height):
        print(f"Tamaño del canvas: {width}x{height}")
        
        # Punto de inicio: centro del borde inferior
        Arbol.POSICION_RAIZ.posicion_x = width / 2
        Arbol.POSICION_RAIZ.posicion_y = height

        self.tamano_canvas = (width, height)



def crea_box_de_juego():
    return JuegoRecursionArbol.obtenerInstanciaSingleton().main_box