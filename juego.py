#!/usr/bin/env python3
from domino import shuffle, take
from jugador import Jugador
from estado import Estado

class domino_cb:
    def __init__(self, elegir, puntos):
        self.elegir = elegir
        self.puntos = puntos

def play(state, cb, gamma=1.0):
    '''Devuelve una lista de puntos conseguidos'''
    if state.pasan==4:
        puntos = state.puntos()
        # El callback es para notificar el estado y la recompensa
        cb.puntos(state, puntos)
        return puntos

    opciones = state.opciones()
    if len(opciones) > 0:
        jugada = cb.elegir(opciones, state.turno)
        
        new_state = state.jugar(jugada)

        if new_state.fin_partida():
            puntos = new_state.puntos()
            cb.puntos(new_state, puntos)
            return puntos

        puntos = play(new_state, cb, gamma) * gamma
        cb.puntos(state, puntos)
        return puntos

    new_state = state.pasar()
    puntos = play(new_state, cb, gamma) * gamma
    cb.puntos(state, puntos)
    return puntos

def play_game(gamma = 1.0):
    
    cb = domino_cb(
        lambda opciones, turno: opciones[0],
        lambda state, puntos: print(state.mesa, puntos)
        )

    mezcla = shuffle()
    j1 = Jugador(0, take(mezcla, 7))
    j2 = Jugador(1, take(mezcla, 7))
    j3 = Jugador(2, take(mezcla, 7))
    j4 = Jugador(3, take(mezcla, 7))

    print(j1.fichas)
    print(j2.fichas)
    print(j3.fichas)
    print(j4.fichas)

    state = Estado([j1, j2, j3,j4])
    print("Puntos antes:", state.puntos())
    
    puntos = play(state, cb, gamma)
    print("Puntos despues: ", puntos)
