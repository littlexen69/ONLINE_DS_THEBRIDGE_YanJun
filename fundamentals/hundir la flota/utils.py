import numpy as np
import random

LADO_TABLERO = 10

def crea_tablero(lado = 10):
    tablero = np.full((lado,lado),"_")
    return tablero

def coloca_barco(tablero, barco):
    for pieza in barco:
        tablero[pieza] = "O"
    return tablero

def disparar(tablero, coordenada):
    if tablero[coordenada] == "O":
        tablero[coordenada] = "X"
        print("Tocado")
    elif tablero[coordenada] == "X" or tablero[coordenada] == "A":
        print("Dispara a otro sitio")
    else:
        tablero[coordenada] = "A"
        print("Agua")

def crear_barco(eslora):
    while True:
        barco = []
        fila = random.randint(0, LADO_TABLERO - 1)
        col = random.randint(0, LADO_TABLERO - 1)
        orientacion = random.choice(["N", "S", "E", "O"])
        barco.append((fila, col))
        for i in range(1, eslora):
            if orientacion == "N":
                fila -= 1
            elif orientacion == "S":
                fila += 1
            elif orientacion == "E":
                col += 1
            elif orientacion == "O":
                col -= 1
            barco.append((fila, col))
        return barco


def es_valido(barco, tablero):
    for fila, col in barco:
        if fila < 0 or fila >= tablero.shape[0] or col < 0 or col >= tablero.shape[1]:
            return False
        if tablero[fila, col] != "_":
            return False
    return True

def colocar_barcos(tablero):
    esloras = [2, 2, 2, 3, 3, 4]

    for eslora in esloras:
        colocado = False
        while not colocado:
            barco = crear_barco(eslora)
            if es_valido(barco, tablero):
                coloca_barco(tablero, barco)
                colocado = True