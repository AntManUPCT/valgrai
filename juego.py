#!/usr/bin/env python3
from domino import shuffle, take, JUGADORES
from jugador import Jugador
from estado import Estado
import random

class domino_cb:
    def __init__(self, elegir, puntos, final):
        self.elegir = elegir
        self.puntos = puntos
        self.final = final

def play(state, cb, gamma=1.0):
    '''Devuelve una lista de puntos conseguidos'''
    if state.pasan==4:
        puntos = state.puntos()
        cb.final(puntos)
        # El callback es para notificar el estado y la recompensa
        cb.puntos(state, puntos)
        return puntos

    opciones = state.opciones()
    if len(opciones) > 0:
        jugada = cb.elegir(state.mesa, state.jugador(), opciones, state.jugada)

        new_state = state.jugar(jugada)

        if new_state.fin_partida():
            puntos = new_state.puntos()
            cb.final(puntos)
            cb.puntos(new_state, puntos)
            puntos *= gamma
            cb.puntos(state, puntos)
            return puntos

        puntos = play(new_state, cb, gamma) * gamma
        cb.puntos(state, puntos)
        return puntos

    new_state = state.pasar()
    puntos = play(new_state, cb, gamma) * gamma
    cb.puntos(state, puntos)
    return puntos

def domino(cb, gamma = 1.0):
    ''' Inicia el juego de una nueva partida de domino '''

    mezcla = shuffle()

    reparto = list(take(mezcla, 7) for i in range(JUGADORES))

    sale = next(i for i,f in enumerate(reparto) if '66' in f)
    resto = list(i for i,f in enumerate(reparto) if '66' not in f)

    j1 = Jugador(0, reparto[sale])
    j2 = Jugador(1, reparto[resto[0]])
    j3 = Jugador(2, reparto[resto[1]])
    j4 = Jugador(3, reparto[resto[2]])

    juegan = [j1, j2, j3,j4]

    state = Estado(jugadores=juegan)

    puntos = play(state, cb, gamma)

if __name__ == "__main__":
    cb = domino_cb(
        lambda mesa, jugadr, opciones, turno: opciones[0],
        lambda state, puntos: print(state.mesa, puntos),
        lambda puntos: print(puntos)
        )

    domino(cb)
