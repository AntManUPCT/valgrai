#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""

from domino import MLEN, JUGADORES, CODG, score_fichas, try_first, try_last
import numpy as np

IMG_ALTO = 50
IMG_ANCHO = MLEN + MLEN + 3
IMG_ITEMS = IMG_ALTO*IMG_ANCHO
LADO_F = MLEN + MLEN
LADO_L = LADO_F + 1
JUGADO = LADO_L + 1

class Jugador:
    
    def __init__(self, turno, fichas, jugado = np.zeros((IMG_ALTO, IMG_ANCHO), dtype='float32')):
        self.fichas = fichas
        self.turno = turno % JUGADORES
        self.jugado = jugado

    def __repr__(self):
        jugado = '\n'.join([''.join(map(lambda x: ' ' if x == 0.0 else '*', f)) for f in self.jugado])
        return 'Jugador('+str(self.turno) + ',\n' + str(self.fichas) + ',\n' + jugado+')'

    def ficha(self, indx):
        return self.fichas[indx]

    def puntos(self):
        return score_fichas(self.fichas)

    def opciones(self, mesa):
        if len(mesa) == 0:
            return [('F', i) for i in range(len(self.fichas))]

        result=[]
        for i in range(len(self.fichas)):
            ficha = self.fichas[i]
            if try_first(ficha, mesa):
                result.append(('F', i))
            if try_last(ficha, mesa):
                result.append(('L', i))
        return result

    def jugar(self, lado, ficha, turno, indx):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        # Si muevo yo quitar la ficha puesta
        if self.turno == (turno % JUGADORES):
            fichas.pop(indx)

        code = CODG[ficha]
        jugado[turno, code] = 1.0
        if lado == 'F':
            jugado[turno, LADO_F] = 1.0
        elif lado == 'L':
            jugado[turno, LADO_L] = 1.0
        jugado[turno, JUGADO] = 1.0

        # Pintar las que me quedan
        for ficha in fichas:
            code = CODG[ficha]
            jugado[turno, MLEN + code] = 1.0

        return Jugador(self.turno, fichas, jugado)

    def pasar(self, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()
        jugado[turno, JUGADO] = 1.0

        # Pintar las que me quedan
        for ficha in self.fichas:
            code = CODG[ficha]
            jugado[turno, MLEN + code] = 1.0
        
        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0

