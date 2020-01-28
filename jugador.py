#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""

from domino import MLEN, JUGADORES, score_fichas, try_first, try_last
import numpy as np

FEATURES = 4 + 7 + 7
JUGADAS = 0
EN_MESA  = JUGADAS + 4
ME_QUEDA = EN_MESA + 7

class Jugador:
    
    def __init__(self, turno, fichas, jugado = None):
        self.fichas = fichas
        self.turno = turno
        if jugado is None:
            self.jugado = np.zeros((FEATURES,), dtype='float32')
        else:
            self.jugado = jugado

        # Contabilizar los puntos que tengo
        if np.sum(self.jugado) == 0.0:
            for f in fichas:
                self.jugado[ME_QUEDA + int(f[0])] += 1.0
                self.jugado[ME_QUEDA + int(f[1])] += 1.0
        
    def __repr__(self):
        return 'Jugador('+str(self.turno) + ',\n' + str(self.fichas) + ',\n' + self.jugado + ')'

    def sale(self):
        return "66" in self.fichas

    def ficha(self, indx):
        return self.fichas[indx]

    def puntos(self):
        return score_fichas(self.fichas)

    def opciones(self, mesa):
        if len(mesa) == 0:
            #return [('F', i) for i in range(len(self.fichas))]
            # Empezar colocando el 6·6
            i = self.fichas.index('66')
            return [('F', i)]

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

        jugado[turno] += 1.0

        n1 = int(ficha[0])
        n2 = int(ficha[1])
        jugado[EN_MESA + n1] += 1.0
        jugado[EN_MESA + n2] += 1.0

        # Si muevo yo quitarme la ficha puesta
        if self.turno == turno:
            fichas.pop(indx)
            jugado[ME_QUEDA + n1] -= 1.0
            jugado[ME_QUEDA + n2] -= 1.0

        return Jugador(self.turno, fichas, jugado)

    def pasar(self, jugada, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()

        jugado[turno] += 1
        
        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0

