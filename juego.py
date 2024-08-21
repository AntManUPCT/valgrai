#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 10:36:35 2019

@author: antonio manuel
"""

from domino import shuffle, take, played, JUGADORES
from jugador import Jugador
from estado import Estado
from resumido import Resumido
from random import randint

class domino_cb:
    def __init__(self, elegir, puntos, final, jugar, pasar):
        self.elegir = elegir  # función para elegir una ficha
        self.puntos = puntos  # función para notificar los puntos obtenidos
        self.final = final  # funcion para notificar el final de la partida
        self.jugar = jugar  # funcion para notificar la ficha jugada por un jugador
        self.pasar = pasar  # funcion para notificar que un jugador pasa en su turno


def fin_partida(state, cb):
    puntos = state.puntos()
    # El callback es para notificar el estado y la recompensa
    cb.final(puntos)          # Notificar final de la partida
    cb.puntos(state, puntos)  # Notificar la recompensa obtenida
    return puntos


def play(state, cb, gamma=1.0):
    '''Devuelve una lista de puntos conseguidos'''
    if state.todos_pasan():
        return fin_partida(state, cb)

    opciones = state.opciones()
    if len(opciones) > 0:
        jugada = cb.elegir(state.mesa, state.jugador(), opciones)
        cb.jugar(state, jugada)

        new_state = state.jugar(jugada)
        if new_state.fin_partida():
            return fin_partida(new_state, cb)

    else:
        new_state = state.pasar()
        cb.pasar(state)

    puntos = play(new_state, cb, gamma) * gamma
    cb.puntos(state, puntos)
    return puntos


def domino(cb, bdmental, gamma=1.0):
    ''' Inicia el juego de una nueva partida de domino '''

    mezcla = shuffle()

    j1 = Jugador(0, take(mezcla, 7), bdmental())
    j2 = Jugador(1, take(mezcla, 7), bdmental())
    j3 = Jugador(2, take(mezcla, 7), bdmental())
    j4 = Jugador(3, take(mezcla, 7), bdmental())

    juegan = [j1, j2, j3, j4]
    empieza = randint(0, JUGADORES - 1)
    state = Estado(jugadores=juegan, juega=empieza)

    return play(state, cb, gamma)


if __name__ == "__main__":
    cb = domino_cb(
        lambda mesa, jugadr, opciones: opciones[0],
        lambda state, puntos: None,
        lambda puntos: print(puntos),
        lambda state, jugada: print(state.jugador().turno, played(jugada)),
        lambda state: print(state.jugador().turno, "Pasa")
    )

    print("Puntos: ", domino(cb))
