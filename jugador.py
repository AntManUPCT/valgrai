#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""


from domino import MAZO, MLEN, CODG, JUGADORES, codes, score_fichas, try_first, try_last
import numpy as np


FILAS = MLEN               # 28 filas
COLAS = 2 * JUGADORES      # 8 columnas
FEATURES = FILAS * COLAS   # 224 atributos

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


class Jugador:

    def __init__(self, turno, fichas, jugado=None):
        self.fichas = fichas
        self.turno = turno
        if jugado is None:
            self.jugado = np.zeros((FILAS, COLAS), dtype='float32')
            # fijar mis fichas y que no tienen los otros jugadores
            for f in fichas:
                fila = CODG[f]
                for j in range(JUGADORES):
                    self.jugado[fila, JUGADORES + j] = 1.0 if j == 0 else -1.0
        else:
            self.jugado = jugado

    def __repr__(self):
        return 'Jugador(' + str(self.turno) + ',\n' + str(self.fichas) + ',\n' + self.jugado + ')'

    def puntos(self):
        return score_fichas(self.fichas)

    # Mis posibles opciones en función de mis fichas
    # Las opciones son un par (LADO, CODIGO_FICHA)
    # LADO = 'F' | 'L'
    # CODIGO_FICHA = x in 1..MLEN
    def opciones(self, mesa):
        if len(mesa) == 0:
            return [('F', i) for i in codes(self.fichas)]

        result = []
        for ficha in self.fichas:
            if try_first(ficha, mesa):
                result.append(('F', CODG[ficha]))
            if try_last(ficha, mesa):
                result.append(('L', CODG[ficha]))
        return result

    # Las posibles opciones de otro jugador en funcion de la información
    # que tengo a partir de las fichas que ha ya puesto o si ha pasado
    def opciones_jugador(self, mesa, jugador):
        if jugador == self.turno:
            return self.opciones(mesa)

        result = []
        for fila in range(MLEN):
            ficha = MAZO[fila]
            if self.jugado[fila, JUGADORES + jugador] > -1:
                if try_first(ficha, mesa):
                    result.append(('F', fila))
                if try_last(ficha, mesa):
                    result.append(('L', fila))
        return result

    def jugar(self, lado, ficha, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        fila = CODG[ficha]
        cola = (turno + JUGADORES - self.turno) % JUGADORES

        jugado[fila, cola] = 1.0  # Ficha puesta en la mesa
        for j in range(JUGADORES):
            jugado[fila, JUGADORES + j] = -1.0  # Nadie tiene ya esta ficha

        # Si muevo yo quitarme la ficha puesta
        if self.turno == turno:
            fichas.remove(ficha)  # quitarla de la nueva copia

        return Jugador(self.turno, fichas, jugado)

    def pasar(self, turno, mesa):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        izda = mesa[0]
        dcha = mesa[-1]
        cola = (turno + JUGADORES - self.turno) % JUGADORES

        # Marcar las fichas que no tiene el jugador que pasa
        for ficha, fila in CODG.items():
            if (izda in ficha) or (dcha in ficha):
                jugado[fila, JUGADORES + cola] = -1.0

        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0
