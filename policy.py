#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from domino import MAZO, PUNTOS

import numpy as np
import random


class QFunction:

    def __init__(self, model):
        self.model = model

    def elegir(self, mesa, jugador, opciones):
        values = np.empty((len(opciones),), dtype='float32')
        for i, (lado, index) in enumerate(opciones):
            # Nuevo estado del jugador tras probar esta accion
            nj = jugador.jugar(lado, MAZO[index], jugador.turno)
            x = nj.estado.get_features()
            y = self.model.predict(x, verbose=0)
            values[i] = y
        return opciones[np.argmax(values)]


class RandomPolicy:

    def elegir(self, mesa, jugador, opciones):
        # Elige una ficha aleatoria
        return random.choice(opciones)


class MaxValuePolicy:

    def elegir(self, mesa, jugador, opciones):
        # Elige la ficha de mayor puntuacion
        values = [PUNTOS[f] for l, f in opciones]
        return opciones[np.argmax(values)]
