#!/usr/bin/env python3
import domino
import juego
from jugador import FEATURES
import policy

import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import os.path

# La funcion choice() seleccionará una accion usando el modelo provisional
# La funcion puntuar() entrenara el modelo con las recompensas obtenidas


class generador:

    def __init__(self, model, bs, gamma=1.0, parejas=False):
        self.model = model
        self.policy = policy.QFunction(model)
        self.bs = bs   # Batch Size
        self.gamma = gamma
        self.parejas = parejas
        self.maxsize = 4 * bs
        self.offset = 0
        self.x_train = np.zeros((self.maxsize, FEATURES), dtype='float32')
        self.y_train = np.zeros((self.maxsize, 1), dtype='float32')
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

        # Generar un elemento de entrenamiento
        self.x_train[self.indx, :] = state.jugadores[juega].jugado.reshape((FEATURES,))
        self.y_train[self.indx, :] = y
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
                juego.domino(self.cb, self.gamma)


def modelo():
    # Modelo basado en red Perceptron Multi Capa
    model = Sequential()
    model.add(Dense(500, activation='relu', input_shape=(FEATURES,)))
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(600, activation='relu'))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    print(model.summary(80))
    if os.path.exists('domino.hdf5'):
        model.load_weights('domino.hdf5')

    return model


def entrenar(model):
    gen = generador(model, 20000, 0.95)  # , True)
    # model.compile(loss='mse', optimizer='sgd')
    # model.compile(loss='mse', optimizer='rmsprop')
    # model.compile(loss='mse', optimizer='adam')
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    # model.compile(loss='mse', optimizer='adadelta')
    history = model.fit_generator(gen.generar(), steps_per_epoch=10, epochs=5000, verbose=1)
    model.save_weights('domino.hdf5')
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
    entrenar(modelo())
