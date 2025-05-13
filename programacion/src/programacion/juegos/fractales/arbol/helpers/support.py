from math import radians, cos, sin, exp
from toga import Canvas
import time
from ..arbol import Arbol, Rama, Posicion



# a mayor k , mas abrupta es la reduccion de grosor ( 0 < k)
def reduce_grosor(nivel, max_grosor=Rama.MAX_GROSOR, k=0.95):
    #print(f"grosor: {max_grosor}*{exp(-k * nivel)} = {max_grosor * exp(-k * nivel)}")
    return max_grosor * exp(-k * nivel)

def rotar_angulo(angulo_actual, paso):
    return (angulo_actual + paso) % 360

def rotar_derecha(angulo_actual):
    return rotar_angulo(angulo_actual, 45)

def rotar_izquierda(angulo_actual):
    return rotar_angulo(angulo_actual, -45)

def destino_del_tronco(x, y, angulo_grados, distancia):
        angulo_rad = radians(angulo_grados)
        x_dest = x + distancia * cos(angulo_rad)
        y_dest = y + distancia * sin(angulo_rad)  # Positivo hacia abajo en canvas
        return x_dest, y_dest


def calcula_dimensiones_de_nivel(canvas_size, r, L0_ratio, hoja_ratio, max_niveles):
    """
    Devuelve una lista con longitud y ancho
    Se detiene cuando no cabe una rama más ni la hoja.
    r cambia ratio reduccion de grosor
    L0 ratio de tamano tronco
    hoja_ratio ratio tamano de hoja

    """
    L0 = L0_ratio * canvas_size
    hoja = hoja_ratio * canvas_size
    suma = 0
    dimensiones = []

    for nivel in range(max_niveles):
        longitud_actual = longitud_nivel(nivel, canvas_size, r=r, L0_ratio=L0_ratio)
        rama_extra = longitud_nivel(nivel + 1, canvas_size, r=r, L0_ratio=L0_ratio)

        if  suma + longitud_actual + rama_extra + hoja >= canvas_size:
            break

        suma += longitud_actual
        dimensiones.append((round(longitud_actual, 2), round(reduce_grosor(nivel))))  # logitud y ancho fijo = 0

    dimensiones.reverse() # para que la más corta esté primero


    print(f"Uso del canvas: {sum([longitud for longitud, grosor in dimensiones])}")

    return dimensiones


def longitud_nivel(nivel, canvas_size, r, L0_ratio):
    """
    Calcula la longitud de la rama en el nivel dado.
    """
    L0 = L0_ratio * canvas_size
    return round(L0 * (r ** nivel), 0)


# calcula el final de un tronco. Y devuelve su posision. El proximo arbol tiene su base ahí.
def mueve_arbol(posic_inicio:Posicion, direccion, nivel):
            angulo_rad = radians(direccion)
            coseno = cos(angulo_rad)
            seno = sin (angulo_rad)
            long = Arbol.DIMENSIONES[nivel][0]
            x_dest = posic_inicio.posicion_x + long * coseno
            y_dest = posic_inicio.posicion_y + long * seno  # Positivo hacia abajo en canvas
            return Posicion(x_dest, y_dest)

def posic_final_rama(posicion, direccion, nivel):
    return mueve_arbol(posicion, direccion, nivel)

def grosor_rama(nivel):
    return Arbol.DIMENSIONES[nivel][1]

def pinta_rama(posicion, direccion, altura, color=Arbol.COLOR):
        with Arbol.CANVAS.Stroke(color=color, line_width=grosor_rama(altura)) as s:
            s.move_to(*posicion.tupla())
            posic_final = posic_final_rama(posicion, direccion, altura)
            posic_final_tupla = posic_final.tupla()
            s.line_to(*posic_final_tupla)      
        #Arbol.CANVAS.redraw()

def pinta_hoja(posicion, color=Arbol.COLOR):
        with Arbol.CANVAS.Fill(color='GREEN') as fill:
            fill.arc(posicion.posicion_x, posicion.posicion_y,Arbol.GROSOR_HOJA)
        #Arbol.CANVAS.redraw()



def pinta_arbol_sync(posicion, direccion, altura):

    t0 = time.time()
    pinta_rama(posicion, direccion, altura)
    
    nueva_posicion = mueve_arbol(posicion, direccion, altura)
        
    if (altura == 0):
        pinta_hoja(nueva_posicion)
    elif (altura > Arbol.ALTURAS - 1):
        pinta_arbol_sync(nueva_posicion, direccion, altura-1)
    else:
        pinta_arbol_sync(nueva_posicion, direccion, altura-1)
        pinta_arbol_sync(nueva_posicion, rotar_derecha(direccion), altura-1)
        pinta_arbol_sync(nueva_posicion, rotar_izquierda(direccion), altura-1)

    if altura == Arbol.ALTURAS:
        print(f"Total sync render time: {time.time() - t0:.2f} s")
