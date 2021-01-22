#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from domino import MAZO
from jugador import FEATURES

import numpy as np


class Estrategia:

    def __init__(self, model):
        self.model = model

    def evaluar(self, jugador, opciones, jugada):
        values = np.empty((len(opciones),), dtype='float32')
        for i, (lado, index) in enumerate(opciones):
            # Nuevo estado del jugador tras probar esta accion
            nj = jugador.jugar(lado, MAZO[index], jugada, jugador.turno)
            x = nj.jugado.reshape((1, FEATURES))
            y = self.model.predict(x)
            values[i] = y
        return values

    def elegir(self, jugador, opciones, jugada):
        ''' Elegir la mejor opcion para este jugador según el modelo '''
        if len(opciones) == 1:
            return opciones[0]

        return opciones[np.argmax(self.evaluar(jugador, opciones, jugada))]
