#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import domino
import juego
import policy
from textual import Textual

import random
import numpy as np
import matplotlib.pyplot as plt
import os.path

import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Embedding, Input, GlobalAveragePooling1D
from tensorflow.keras.models import Model

from domino import WORDS

# La funcion choice() seleccionará una accion usando el modelo provisional
# La funcion puntuar() entrenara el modelo con las recompensas obtenidas

palabras = [' '.join(WORDS)]
max_len = 50 # Longitud máxima de una partida
fichero_pesos = './pesos/valgrai/transfo/domino.weights.h5'

class generador:

    def __init__(self, model, max_len, bdmental, bs, gamma=1.0, parejas=False):
        self.model = model
        self.bdmental = bdmental
        self.bs = bs   # Batch Size
        self.gamma = gamma
        self.parejas = parejas
        self.maxsize = 4 * bs
        self.offset = 0
        self.x_train = np.zeros((self.maxsize, max_len), dtype='float32')
        self.y_train = np.zeros((self.maxsize, 2), dtype='float32')
        self.indx = 0
        self.dc = 0
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=50) # len(WORDS)+1)
        self.tokenizer.fit_on_texts(palabras)
        self.policy = policy.Transfo_QFunction(model, self.tokenizer)
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
        texto = [' '.join(state.jugadores[juega].estado.get_features())]
        # Pasarla por el 'tokenizer'
        secuencia = self.tokenizer.texts_to_sequences(texto)
        # Ajustar las secuencias para tener la misma longitud
        padded = tf.keras.preprocessing.sequence.pad_sequences(secuencia, maxlen=50)

        # Generar un elemento de entrenamiento
        self.x_train[self.indx, :] = padded
        self.y_train[self.indx, :] = [y, 1.0 - y] # (prob ganar, prob perder)
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


# Parámetros de configuracion para el transformer
vocab_size = 50  # Tamaño del vocabulario
embed_dim = 64
num_heads = 4
ff_dim = 32
rate = 0.1 # Dropout rate = 0.1 (10%)

# Definir una capa de Transformer Encoder
class TransformerEncoder(Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerEncoder, self).__init__()
        self.attention = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.ffn = tf.keras.Sequential(
            [Dense(ff_dim, activation="relu"), Dense(embed_dim)]
        )
        self.dropout2 = tf.keras.layers.Dropout(rate)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training):
        attn_output = self.attention(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        out2 = self.layernorm2(out1 + ffn_output)
        return out2


def modelo(training):
    # Capa de entrada
    inputs = Input(shape=(max_len,))

    # Capa de incrustación
    embedding_layer = Embedding(vocab_size, embed_dim)
    x = embedding_layer(inputs)

    # Capa Transformer
    transformer_layer = TransformerEncoder(embed_dim, num_heads=num_heads, ff_dim=ff_dim, rate=0.1)
    x = transformer_layer(x, training=training)

    # Capa de salida
    x = tf.keras.layers.GlobalAveragePooling1D()(x)
    x = Dense(20, activation="relu")(x)
    outputs = Dense(2, activation="softmax")(x)  # Para clasificación binaria

    # Crear el modelo
    model = Model(inputs=inputs, outputs=outputs)

    model.summary(80)

    if os.path.exists(fichero_pesos):
        model.load_weights(fichero_pesos)

    return model


def entrenar(model, max_len, bdmental):
    gen = generador(model, max_len, bdmental, 1000, 0.95)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(gen.generar(), steps_per_epoch=10, epochs=50, verbose=1)
    model.save_weights(fichero_pesos)
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
    bdmental = [Textual, Textual, Textual, Textual]
    entrenar(modelo(True), max_len, bdmental)
