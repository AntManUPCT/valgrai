#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado el martes 5 de enero de 2021 a las 13:56

@author: antonio manuel
"""

from domino import JUGADORES, poner_ficha, played
from jugador import FEATURES
import juego
from entrenar import modelo
from sys import float_info

MAX_DEEP_LEVEL = 5

# En estas funciones el jugador es el que se está evaluando
# El turno es el identificador de al que le toca jugar


class MiniMax:

    def __init__(self, model):
        self.model = model

    def valoracion_final(self, jugadr):
        # Evaluar con la RN el estado alcanzado en la nueva mesa
        return self.model.predict(jugadr.reshape((1, FEATURES)))

    def seguir_jugando(self, mesa, jugadr, turno, deep_level):
        # Valorar recursivamente las jugadas del resto de jugadores
        siguiente = (turno + 1) % JUGADORES

        # Opciones que puede tener el siguiente jugador
        opciones = jugadr.opciones_jugador(mesa, siguiente)
        if len(opciones) == 0:
            return self.valorar_pasar(mesa, jugadr, turno, deep_level)

        if jugadr.turno == turno:
            return self.maximizar(mesa, jugadr, opciones, siguiente, deep_level)
        else:
            return self.minimizar(mesa, jugadr, opciones, siguiente, deep_level)

    def valorar_jugar(self, mesa, jugadr, turno, opcion, deep_level):
        # Poner la ficha jugada en la mesa
        lado, ficha = played(opcion)
        nueva_mesa = poner_ficha(mesa, lado, ficha)

        print("MinMax:", nueva_mesa)

        if deep_level == 0:
            return self.valoracion_final(mesa, jugadr)

        # Información conocida del resto de jugadores en caso de que
        # este haga uso de esta opción.
        nuevo_jugador = jugadr.jugar(lado, ficha, turno)

        return self.seguir_jugando(nueva_mesa, nuevo_jugador, turno, deep_level - 1)

    def valorar_pasar(self, mesa, jugadr, turno, deep_level):
        # Información conocida del resto de jugadores en caso de que este pase
        nuevo_jugador = jugadr.pasar(turno, mesa)

        print("MinMax:", mesa)

        if deep_level == 0:
            return self.valoracion_final(mesa, nuevo_jugador)

        return self.seguir_jugando(mesa, nuevo_jugador, turno, deep_level - 1)

    def maximizar(self, mesa, jugadr, opciones, turno, deep_level):
        e = opciones[0]   # eleccion
        v = -float_info.max  # valoracion de la eleccion
        for o in opciones:
            nv = self.valorar_jugar(mesa, jugadr, turno, o, deep_level - 1)
            if nv > v:
                v = nv
                e = o

        # devolver siempre la opción que produce la mayor valoración
        return e

    def minimizar(self, mesa, jugadr, opciones, turno, deep_level):
        e = opciones[0]   # eleccion
        v = float_info.max  # valoracion de la eleccion
        for o in opciones:
            nv = self.valorar_jugar(mesa, jugadr, turno, o, deep_level - 1)
            if nv < v:
                v = nv
                e = o

        # devolver siempre la opción que produce la menor valoración
        return e

    def elegir(self, mesa, jugadr, opciones, turno):
        # Aquí siempre hay al menos una opcion

        if len(opciones) == 1:
            return opciones[0]  # Solo hay una opcion, elegir esa

        # Aplicar MinMax cuando hay al menos dos opciones
        # Busqueda en profundidad, se empieza maximizando las opciones del jugador
        return self.maximizar(mesa, jugadr, opciones, turno, MAX_DEEP_LEVEL)


def puntuar(state, puntos):
    None


def terminar(puntos):
    pass


def jugar(state, jugada):
    pass


def pasar(state):
    pass


if __name__ == "__main__":

    minimax = MiniMax(modelo())

    def elegir(mesa, jugadr, opciones, turno):
        return minimax.elegir(mesa, jugadr, opciones, turno)

    cb = juego.domino_cb(elegir, puntuar, terminar, jugar, pasar)

    juego.domino(cb, gamma=1.0)
