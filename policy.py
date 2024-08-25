#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from domino import MAZO, PUNTOS

import tensorflow as tf
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

class Transfo_QFunction:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def elegir(self, mesa, jugador, opciones):
        # llegan en bloques de 32 en 32
        values = np.empty((len(opciones),), dtype='float32')
        for i, (lado, index) in enumerate(opciones):
            # Nuevo estado del jugador tras probar esta accion
            nj = jugador.jugar(lado, MAZO[index], jugador.turno)
            # construir el texto de entrada
            texto = [' '.join(nj.estado.get_features())]
            # Pasarla por el 'tokenizer'
            secuencia = self.tokenizer.texts_to_sequences(texto)
            # Ajustar las secuencias para tener la misma longitud
            x = tf.keras.preprocessing.sequence.pad_sequences(secuencia, maxlen=50)
            y = self.model.predict(x, verbose=0)
            values[i] = y[0][0]
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
