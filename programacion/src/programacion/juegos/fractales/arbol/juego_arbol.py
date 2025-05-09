import toga
from toga import Canvas
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio

from .helpers.support import *
from .arbol import Arbol, Rama, Hoja, Posicion


class JuegoRecursionArbol(toga.App):

    MAX_NUM_ALTURAS = 3
    MAX_GROSOR = 100

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
        
        self.posicion_inicial = Posicion(0,0)
        self.velocidad = 0

        self.running = True
        

        btn_restart = toga.Button("Pinta ! ", on_press=self.restart_game, style=Pack(width=80, height=40))
        self.slider_velocidad = toga.Slider("velocidad", value=0, min=0, max=1, on_release=self.muestra_velocidad)
        self.pre_recursion = toga.Switch("pinta_antes", value = True)
        controls = toga.Box(style=Pack(direction=ROW))
        controls.add(self.slider_velocidad)
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


    def limpia_canvas(self):
        with self.canvas.Fill(color="WHITE") as fill:
            fill.rect(0,0,self.tamano_canvas[0],self.tamano_canvas[1])

    async def restart_game(self, widget):

        self.limpia_canvas()
        nivel = Arbol.NUM_ALTURAS

        self.arbol = self.fabrica_arbol(Rama(Rama.HACIA_ARRIBA, self.posicion_inicial, nivel), self.canvas, nivel)

        asyncio.get_event_loop().create_task(
            self.crea_arbol(Rama(Rama.HACIA_ARRIBA, self.posicion_inicial, nivel), self.canvas, nivel))
        
#        asyncio.get_event_loop().create_task(
#            self.pinta_arbol(self.posicion_inicial.posicion_x,self.posicion_inicial.posicion_y, 
#                                -90, JuegoRecursionArbol.MAX_GROSOR, 0)
#                                )
        self.canvas.redraw()
        return


    ################################
    # métodos para pintar el árbol #
    ################################

    def cambiar_punto_inicio(self, canvas, width, height):
        print(f"Tamaño del canvas: {width}x{height}")
        
        # Punto de inicio: centro del borde inferior
        self.posicion_inicial.posicion_x = width / 2
        self.posicion_inicial.posicion_y = height

        self.tamano_canvas = (width, height)

    # recorre usando la estructura
    def fabrica_arbol(self, rama:Rama, numero_alturas):


        rama.nivel = numero_alturas
        
        if (numero_alturas == 0):
            rama.hoja = Hoja(rama.posicion_final)

        elif (numero_alturas > Arbol.NUM_ALTURAS - 2):
            rama.rama_centro = self.fabrica_arbol(Rama(rama.direccion, rama.posicion_final, numero_alturas-1), numero_alturas - 1)
        else:
            rama.rama_centro = self.fabrica_arbol(Rama(rama.direccion, rama.posicion_final, numero_alturas-1),  numero_alturas - 1)
            rama.rama_derecha = self.fabrica_arbol(Rama(rotar_derecha(rama.direccion), rama.posicion_final, numero_alturas-1), numero_alturas - 1)
            rama.rama_izquierda = self.fabrica_arbol(Rama(rotar_izquierda(rama.direccion), rama.posicion_final, numero_alturas-1), numero_alturas - 1)


        return rama 

    # recorre usando la estructura
    async def crea_arbol(self, rama:Rama, canvas, numero_alturas):

    # tengo que pasar el objeto de la velocidad (slider) => Pasar la funcion crea_arbol a juego_arbol.py   
        if (self.slider_velocidad.value >0):
            await asyncio.sleep(self.slider_velocidad.value)
        canvas.window.content.refresh()

        rama.nivel = numero_alturas
        if (self.pre_recursion.value):
            rama.pintate(canvas)
        
        if (numero_alturas == 0):
            rama.hoja = Hoja(rama.posicion_final)
            rama.hoja.pintate(canvas)
        elif (numero_alturas > Arbol.NUM_ALTURAS - 2):
            rama.rama_centro = await self.crea_arbol(Rama(rama.direccion, rama.posicion_final, numero_alturas-1), canvas, numero_alturas - 1)
        else:
            rama.rama_centro = await self.crea_arbol(Rama(rama.direccion, rama.posicion_final, numero_alturas-1), canvas, numero_alturas - 1)
            rama.rama_derecha = await self.crea_arbol(Rama(rotar_derecha(rama.direccion), rama.posicion_final, numero_alturas-1), canvas, numero_alturas - 1)
            rama.rama_izquierda = await self.crea_arbol(Rama(rotar_izquierda(rama.direccion), rama.posicion_final, numero_alturas-1), canvas, numero_alturas - 1)
        
        
        if (not self.pre_recursion.value):
            rama.pintate(canvas)

        return rama 

    
    def pinta_rama(self, x_inicio, y_inicio, angulo, longitud, nivel):

        x_fin, y_fin = destino_del_tronco(x_inicio, y_inicio, angulo, longitud)
        with self.canvas.Stroke('blue', line_width=reduce_grosor(nivel, JuegoRecursionArbol.MAX_GROSOR)) as s:
            s.move_to(x_inicio, y_inicio)
            s.line_to(x_fin, y_fin)
        
        self.canvas.redraw()
        return x_fin, y_fin 
    

    def pinta_hoja(self, x_inicio, y_inicio):

        with self.canvas.Fillill(color='GREEN') as fill:
            fill.arc(x_inicio, y_inicio, 5)

        self.canvas.redraw()



def crea_box_de_juego():
    return JuegoRecursionArbol.obtenerInstanciaSingleton().main_box