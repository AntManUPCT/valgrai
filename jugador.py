#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""

from domino import MLEN, CODG, JUGADORES, score_fichas, try_first, try_last
import numpy as np

FILAS = MLEN
COLAS = 2*JUGADORES
FEATURES = FILAS * COLAS

class Jugador:

    def __init__(self, turno, fichas, jugado = None):
        self.fichas = fichas
        self.turno = turno
        if jugado is None:
            self.jugado = np.zeros((FILAS, COLAS), dtype='float32')
            for f in fichas:
                for j in range(JUGADORES):
                    self.jugado[CODG[f], JUGADORES + j] = 1.0 if j == turno else -1.0

        else:
            self.jugado = jugado

    def __repr__(self):
        return 'Jugador('+str(self.turno) + ',\n' + str(self.fichas) + ',\n' + self.jugado + ')'

    def ficha(self, indx):
        return self.fichas[indx]

    def puntos(self):
        return score_fichas(self.fichas)

    def opciones(self, mesa):
        if len(mesa) == 0:
            i = self.fichas.index('66')
            return [('F', i)]

        result=[]
        for i, ficha in enumerate(self.fichas):
            if try_first(ficha, mesa):
                result.append(('F', i))
            if try_last(ficha, mesa):
                result.append(('L', i))
        return result

    def jugar(self, lado, ficha, jugada, indx, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        fila = CODG[ficha]
        cola = (turno + JUGADORES - self.turno) % JUGADORES

        jugado[fila, cola] = 1.0
        for j in range(JUGADORES):
            jugado[fila, JUGADORES + j] = -1.0 # Nadie tiene ya esta ficha

        # Si muevo yo quitarme la ficha puesta
        if self.turno == turno:
            fichas.pop(indx) # quitarla de la nueva copia

        return Jugador(self.turno, fichas, jugado)

    def pasar(self, jugada, turno, mesa):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        izda = mesa[0]
        dcha = mesa[-1]
        cola = (turno + JUGADORES - self.turno) % JUGADORES

        # Marcar las fichas que no tiene el jugador que pasa
        for ficha, fila in CODG.items():
            if (izda in ficha) or (dcha in ficha):
                jugado[fila, cola] = -1.0

        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0
