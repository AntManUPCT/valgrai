#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from domino import MAZO
from jugador import FEATURES

import numpy as np


class Qfunction:

    def __init__(self, model):
        self.model = model

    def elegir(self, mesa, jugador, opciones):
        values = np.empty((len(opciones),), dtype='float32')
        for i, (lado, index) in enumerate(opciones):
            # Nuevo estado del jugador tras probar esta accion
            nj = jugador.jugar(lado, MAZO[index], jugador.turno)
            x = nj.jugado.reshape((1, FEATURES))
            y = self.model.predict(x)
            values[i] = y
        return values
