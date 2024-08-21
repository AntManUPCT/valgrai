#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import domino
import juego
from resumido import Resumido
from textual import Textual

def elegir_ficha(mesa, jugador, opciones):
    return opciones[0]

def puntos_conseguidos(estado, puntos):
    return None

def fin_juego(puntos):
    #print(puntos)
    pass

def juega(estado, jugada):
    mostrar_promt(estado)
    # buscar_mas_larga(estado)

def pasa(estado):
    mostrar_promt(estado)
    # buscar_mas_larga(estado)

mas_larga = 0

def buscar_mas_larga(estado):
    global mas_larga
    if estado.jugada > mas_larga:
        mas_larga = estado.jugada
        print('Mas larga: ', mas_larga)
    return None

def mostrar_promt(estado):
    print(estado.jugador().estado.get_features())

if __name__ == '__main__':

    cb = juego.domino_cb(
        elegir_ficha,
        puntos_conseguidos,
        fin_juego,
        juega,
        pasa
    )

    for _ in range(10):
        juego.domino(cb, Textual)
