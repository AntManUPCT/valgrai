#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:32:50 2020

@author: manuel
"""

from domino import CODG, JUGADORES, codes, score_fichas, try_first, try_last
from bdmental import BDMental
import numpy as np

class Jugador:

    def __init__(self, turno, fichas, estado):
        self.fichas = fichas
        self.turno = turno
        self.estado = estado
        self.estado.init(fichas)

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
            return [('IZDA', i) for i in codes(self.fichas)]

        result = []
        for ficha in self.fichas:
            if try_first(ficha, mesa):
                result.append(('IZDA', CODG[ficha]))
            if try_last(ficha, mesa):
                result.append(('DCHA', CODG[ficha]))
        return result

    def jugar(self, lado, ficha, turno):
        fichas = self.fichas.copy()
        estado = self.estado.copy()

        estado.ficha_puesta(ficha, lado, (turno + JUGADORES - self.turno) % JUGADORES)

        # Si muevo yo quitarme la ficha puesta
        if self.turno == turno:
            fichas.remove(ficha)  # quitarla de la nueva copia

        return Jugador(self.turno, fichas, estado)

    def pasar(self, turno, mesa):
        fichas = self.fichas.copy()
        estado = self.estado.copy()

        estado.jugador_pasa(mesa, (turno + JUGADORES - self.turno) % JUGADORES)

        return Jugador(self.turno, fichas, estado)

    def fin(self):
        return len(self.fichas) == 0
