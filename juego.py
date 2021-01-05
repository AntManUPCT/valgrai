#!/usr/bin/env python3
from domino import shuffle, take, JUGADORES
from jugador import Jugador
from estado import Estado


class domino_cb:
    def __init__(self, elegir, puntos, final):
        self.elegir = elegir
        self.puntos = puntos
        self.final = final


def play(state, cb, gamma=1.0):
    '''Devuelve una lista de puntos conseguidos'''
    if state.pasan == 4:
        puntos = state.puntos()
        # El callback es para notificar el estado y la recompensa
        cb.final(puntos)
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


def domino(cb, gamma=1.0):
    ''' Inicia el juego de una nueva partida de domino '''

    mezcla = shuffle()

    j1 = Jugador(0, take(mezcla, 7))
    j2 = Jugador(1, take(mezcla, 7))
    j3 = Jugador(2, take(mezcla, 7))
    j4 = Jugador(3, take(mezcla, 7))

    juegan = [j1, j2, j3, j4]

    state = Estado(jugadores=juegan)

    return play(state, cb, gamma)


if __name__ == "__main__":
    cb = domino_cb(
        lambda mesa, jugadr, opciones, turno: opciones[0],
        lambda state, puntos: print(state.mesa),
        lambda puntos: print(puntos)
    )

    print("Puntos: ", domino(cb))
