#!/usr/bin/env python3

import juego
import entrenar
import estrategia
import minimax

from domino import PUNTOS

import numpy as np
import random


class comparador:

    def __init__(self, policy):
        self.policy = policy
        self.contadores = np.zeros((4,), dtype='int32')

    def eleccion(self, mesa, jugador, opciones):
        # Ordenador contra tres jugadores aleatorios
        if jugador.turno == 0:
            # Elige una ficha aleatoria
            return random.choice(opciones)

        elif jugador.turno == 1:
            # Elige una ficha aleatoria
            return random.choice(opciones)

        elif jugador.turno == 2:
            # Elige la ficha de mayor puntuacion
            values = [PUNTOS[f] for l, f in opciones]
            return opciones[np.argmax(values)]

        elif jugador.turno == 3:
            # ORDENADOR
            values = self.policy.elegir(mesa, jugador, opciones)
            return opciones[np.argmax(values)]

    def finpartida(self, puntos):
        minpuntos = np.min(puntos)
        for i, p in enumerate(puntos):
            if p == minpuntos:
                self.contadores[i] += 1

    def jugar(self):
        cb = juego.domino_cb(
            self.eleccion,
            lambda state, puntos: None,
            self.finpartida,
            lambda state, jugada: None,
            lambda state: None
        )
        juego.domino(cb)


if __name__ == '__main__':

    # Cargar el modelo entrenado
    model = entrenar.modelo()
    model.load_weights('domino.hdf5')

    # Crear una estrategia para el jugador listo
    policyQfunct = estrategia.Qfunction(model)
    policyMinMax = minimax.MiniMax(model)

    # Crear el verificador del modelo
    comp = comparador(policyMinMax)

    # Jugar contra otros tres jugadores
    for i in range(100000):
        comp.jugar()
        if i % 1000 == 0:
            print(i, comp.contadores, end='\r')

    print('Ganadas: ', comp.contadores)
    suma = sum(comp.contadores)
    ratios = np.round(np.array(comp.contadores) * 100.0 / suma, 1)
    print('Ratios.: ', ratios)
