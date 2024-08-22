#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import domino
import juego
import policy
from texual import Textual

import random
import numpy as np
import matplotlib.pyplot as plt
import os.path

import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, TransformerEncoder, Dense
from tensorflow.keras.models import Model

from domino import WORDS

# La funcion choice() seleccionará una accion usando el modelo provisional
# La funcion puntuar() entrenara el modelo con las recompensas obtenidas


class generador:

    def __init__(self, model, bdmental, bs, gamma=1.0, parejas=False):
        self.model = model
        self.bdmental = bdmental
        self.policy = policy.QFunction(model)
        self.bs = bs   # Batch Size
        self.gamma = gamma
        self.parejas = parejas
        self.maxsize = 4 * bs
        self.offset = 0
        self.x_train = np.zeros((self.maxsize, bdmental.num_features()), dtype='float32')
        self.y_train = np.zeros((self.maxsize, 2), dtype='float32')
        self.indx = 0
        self.dc = 0
        self.cb = juego.domino_cb(
            self.eleccion,               # Callback para elegir una ficha a jugar
            self.recompensa,             # Callback para obtener la recompensa
            self.finpartida,
            lambda state, jugada: None,
            lambda state: None
        )

    def eleccion(self, mesa, jugador, opciones):
        if random.random() > 0.9:
            return random.choice(opciones)
        else:
            return self.policy.elegir(mesa, jugador, opciones)

    def recompensa(self, state, puntos):
        juega = state.juega        # Indice del jugador que le toca jugar
        gana1 = np.argmin(puntos)  # Indice del jugador que ganaria ahora
        y = 1.0 if juega == gana1 else 0.0  # recompensa, ¿gano yo?

        if self.parejas:  # ¿gano yo o gana mi compañero?
            gana2 = (gana1 + 2) % domino.JUGADORES
            y = 1.0 if juega == gana1 or juega == gana2 else 0.0

        # construir el texto de entrada
        texto = ' '.join(state.jugadores[juega].estado.get_features())
        # Pasarla por el 'tokenizer'
        secuencia = tokenizer.texts_to_sequences(texto)
        # Ajustar las secuencias para tener la misma longitud
        padded = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=50)

        # Generar un elemento de entrenamiento
        self.x_train[self.indx, :] = padded
        self.y_train[self.indx, :] = [y, 1.0 - y]
        self.indx = (self.indx + 1) % self.maxsize  # Indice en el buffer circular
        self.dc += 1  # data counter

    def finpartida(self, puntos):
        pass

    def generar(self):
        "Generar datos de entrenamiento indefinidamente echando partidas"
        while True:
            while self.dc >= self.bs:
                first = self.offset
                last = first + self.bs
                self.offset = last % self.maxsize
                self.dc -= self.bs
                yield self.x_train[first:last, :], self.y_train[first:last, :]

            while self.dc < self.bs:
                juego.domino(self.cb, self.bdmental, self.gamma)


def modelo(features):
    # Modelo basado en red Perceptron Multi Capa
    model = Sequential()


    model.summary(80)
    if os.path.exists('transfo.domino.hdf5'):
        model.load_weights('transfo.domino.hdf5')

    return model


def entrenar(model, bdmental):
    gen = generador(model, bdmental, 1000, 0.95)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(gen.generar(), steps_per_epoch=10, epochs=50, verbose=1)
    model.save_weights('domino.weights.h5')
    graficar(history)


def graficar(history):
    hdict = history.history
    loss = hdict['loss']
    epochs = range(1, len(loss) + 1)

    plt.plot(epochs, loss, 'b', label='Loss')
    plt.title('Error de entrenamiento')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.show()


if __name__ == "__main__":
    bdmental = Resumido
    entrenar(modelo(bdmental.num_features()), bdmental)
