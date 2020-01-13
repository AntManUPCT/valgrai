#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:36:35 2020

@author: manuel
"""

from domino import JUGADORES, poner_ficha
import numpy as np

class Estado:
    '''
    El estado del juego viene determinado por las fichas que tiene
    cada jugador y la información de lo que han puesto los otros
    jugadores en las jugadas anteriores
    '''

    def __init__(self, jugadores, turno=0, pasan=0, mesa=''):
        self.jugadores = jugadores
        self.turno = turno
        self.pasan = pasan
        self.mesa = mesa

    def __repr__(self):
        return 'Estado(\n' + '\n'.join(map(str, self.jugadores)) + ',\n' + str(self.turno) + ',\n' + str(self.pasan) + ',\n"' + self.mesa + '")'

    def jugador(self):
        indx = self.turno % JUGADORES
        return self.jugadores[indx]

    def puntos(self):
        return np.array([j.puntos() for j in self.jugadores], dtype='float32')

    def opciones(self):
        return self.jugador().opciones(self.mesa)

    def jugar(self, jugada):
        ''' Devolver el nuevo estado '''
        lado = jugada[0]
        indx = jugada[1]
        ficha = self.jugador().ficha(indx)

        jugadores = [j.jugar(lado, ficha, self.turno, indx) for j in self.jugadores]
        mesa = poner_ficha(self.mesa, lado, ficha)
        return Estado(jugadores, self.turno + 1, 0, mesa)

    def pasar(self):
        ''' Devolver el nuevo estado '''
        jugadores = [j.pasar(self.turno) for j in self.jugadores]
        return Estado(jugadores, self.turno + 1, self.pasan + 1, self.mesa)

    def fin_partida(self):
        return any(map(lambda j: j.fin(), self.jugadores))
