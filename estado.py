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

    def __init__(self, jugadores, jugada=0, pasan=0, mesa='', juega=0):
        self.jugadores = jugadores # Lista de los 4 jugadores
        self.jugada = jugada # Siempre incrementa, cuenta las fichas jugadas
        self.pasan = pasan   # Cuenta los jugadores que han pasado
        self.mesa = mesa     # Cadena de caracteres con las fichas sobre la mesa
        self.juega = juega   # Indice de a quien le toca jugar (contador modulo 4)

    def __repr__(self):
        return 'Estado(\n' + '\n'.join(map(str, self.jugadores)) + ',\n' + str(self.jugada) + ',\n' + str(self.pasan) + ',\n"' + self.mesa + '")'

    def jugador(self):
        return self.jugadores[self.juega]

    def puntos(self):
        return np.array([j.puntos() for j in self.jugadores], dtype='float32')

    def opciones(self):
        return self.jugador().opciones(self.mesa)

    def jugar(self, jugada):
        ''' Devolver el nuevo estado '''
        lado, indx = jugada
        ficha = self.jugador().ficha(indx)

        jugadores = [j.jugar(lado, ficha, self.jugada, indx, self.juega) for j in self.jugadores]
        mesa = poner_ficha(self.mesa, lado, ficha)
        siguiente = (self.juega + 1) % JUGADORES
        return Estado(jugadores, self.jugada + 1, 0, mesa, siguiente)

    def pasar(self):
        ''' Devolver el nuevo estado '''
        jugadores = [j.pasar(self.jugada) for j in self.jugadores]
        siguiente = (self.juega + 1) % JUGADORES
        return Estado(jugadores, self.jugada + 1, self.pasan + 1, self.mesa, siguiente)

    def fin_partida(self):
        return any(map(lambda j: j.fin(), self.jugadores))
