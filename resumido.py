#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Ago 20 23:29:50 2024

@author: antonio manuel
"""

from bdmental import BDMental
from domino import MLEN, CODG, JUGADORES
import numpy as np

"""
El estado de cada jugador esta compuesto por:
  1. Bloque de fichas puestas por cada jugador.
     Cada columna es para un jugador (yo, siguiente, siguiente, siguiente)
     Cada fila es para una ficha (0-27)
  2. Bloque con las fichas que tiene o NO tiene ese jugador

Cada jugador tiene un resumen de la información que el conoce de los otros
--------Jugador--
Ficha-|-0123-0123
  00  | 0000 SNNN : Yo tengo una ficha, los otros jugadores no
  01  | 1000 NNNN : Una ficha puesta ya no la tiene nadie
  02  | 0000 ---N : Si un jugador pasa habiendo doses -> no tiene esta ficha
  03  | 0000 N--- : De esta ficha no se nada, ni la tengo ni ha sido puesta
  ..  |
  11  | 0000 SNNN
  12  | 0010 NNNN
  ..  |
  56  | 0000 N---
  66  | 0100 NNNN

Al principio:
  Yo solo tengo las mias y no tengo las demás.
  Los demas no tienen mis fichas y no se sabe nada de las que tienen

En cada jugada:
  Los otros no tienen las fichas que se van poniendo
  Si uno pasa, ese no tiene ninguna de las fichas con las que pasa

PENDIENTE: Seria posible deducir para un jugador las fichas que tiene
si se sabe que todos demás no la tienen. Se podria entrenar una RN
para deducir las posibles fichas que tiene cada jugador
"""

class Resumido(BDMental):

    FILAS = MLEN               # 28 filas
    COLAS = 2 * JUGADORES      # 8 columnas
    FEATURES = FILAS * COLAS   # 224 atributos

    @classmethod
    def num_features(cls):
        return cls.FEATURES

    def __init__(self, clon=None):
        if clon is None:
            self.estado = np.zeros((self.FILAS, self.COLAS), dtype='float32')
        else:
            self.estado = clon

    def init(self, fichas):
        # fijar mis fichas y que no tienen los otros jugadores
        for f in fichas:
            fila = CODG[f]
            for j in range(JUGADORES):
                self.estado[fila, JUGADORES + j] = 1.0 if j == 0 else -1.0

    def copy(self):
        return Resumido(self.estado.copy()) # No crear, se le pasa un clon

    def ficha_puesta(self, ficha, lado, jugador):
        fila = CODG[ficha]
        cola = jugador

        self.estado[fila, cola] = 1.0  # Ficha puesta en la mesa
        for j in range(JUGADORES):
            self.estado[fila, JUGADORES + j] = -1.0  # Nadie tiene ya esta ficha


    def jugador_pasa(self, mesa, jugador):
        izda = mesa[0]
        dcha = mesa[-1]
        cola = jugador

        # Marcar las fichas que no tiene el jugador que pasa
        for ficha, fila in CODG.items():
            if (izda in ficha) or (dcha in ficha):
                self.estado[fila, JUGADORES + cola] = -1.0

    def get_features(self):
        return self.estado.reshape((1, self.FEATURES))
