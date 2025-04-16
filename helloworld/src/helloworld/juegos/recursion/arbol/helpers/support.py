from math import radians, cos, sin


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