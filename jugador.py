#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""

from domino import MLEN, CODG, JUGADORES, score_fichas, try_first, try_last
import numpy as np

FILAS = MLEN
COLAS = JUGADORES + 1
FEATURES = FILAS * COLAS
ME_QUEDA = JUGADORES

class Jugador:
    
    def __init__(self, turno, fichas, jugado = None):
        self.fichas = fichas
        self.turno = turno
        if jugado is None:
            self.jugado = np.zeros((FILAS, COLAS), dtype='float32')
            for f in fichas:
                self.jugado[CODG[f], ME_QUEDA] = 1.0
        else:
            self.jugado = jugado

    def __repr__(self):
        return 'Jugador('+str(self.turno) + ',\n' + str(self.fichas) + ',\n' + self.jugado + ')'

    def ficha(self, indx):
        return self.fichas[indx]

    def puntos(self):
        return score_fichas(self.fichas)

    def opciones(self, mesa):
        result=[]
        for i in range(len(self.fichas)):
            ficha = self.fichas[i]
            if try_first(ficha, mesa):
                result.append(('F', i))
            if try_last(ficha, mesa):
                result.append(('L', i))
        return result

    def jugar(self, lado, ficha, jugada, indx, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        fila = CODG[ficha]
        jugado[fila, turno] = 1.0

        # Si muevo yo quitarme la ficha puesta
        if self.turno == turno:
            jugado[fila, ME_QUEDA] = 0.0
            fichas.pop(indx) # quitarla de la nueva copia

        return Jugador(self.turno, fichas, jugado)

    def pasar(self, jugada, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0

