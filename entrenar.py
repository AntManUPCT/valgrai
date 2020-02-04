#!/usr/bin/env python3
import domino
import juego
from jugador import FEATURES
import estrategia

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
        self.policy = estrategia.Estrategia(model)
        self.bs = bs
        self.gamma = gamma
        self.parejas = parejas
        self.maxsize = 4*bs
        self.offset = 0
        self.x_train = np.zeros((self.maxsize, FEATURES), dtype='float32')
        self.y_train = np.zeros((self.maxsize, 1), dtype='float32')
        self.indx = 0
        self.dc = 0
        self.cb = juego.domino_cb(self.eleccion, self.recompensa, self.salida, self.finpartida)

    def salida(self, sale):
        pass

    def eleccion(self, mesa, jugador, opciones, jugada):
        if random.random() > 0.8:
            return random.choice(opciones)
        else:
            return self.policy.elegir(jugador, opciones, jugada)

    def recompensa(self, state, puntos):
        juega = state.juega # Indice del jugador que le toca jugar
        gana1 = np.argmin(puntos)
        y = 1.0 if juega == gana1 else 0.0

        if self.parejas:
            gana2 = (gana1 + 2) % domino.JUGADORES
            y = 1.0 if juega == gana1 or juega == gana2 else 0.0

        self.x_train[self.indx, :] = state.jugadores[juega].jugado.reshape((FEATURES,))
        self.y_train[self.indx, :] = y
        self.indx = (self.indx + 1) % self.maxsize # Indice en el buffer circular
        self.dc += 1 # data counter

    def finpartida(self, puntos):
        pass

    def generar(self):
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
    model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    print(model.summary(80))
    if os.path.exists('domino.hdf5'):
        model.load_weights('domino.hdf5')

    return model

def entrenar(model):
    gen = generador(model, 5000, 0.95) #, True)
    #model.compile(loss='mse', optimizer='sgd')
    #model.compile(loss='mse', optimizer='rmsprop')
    model.compile(loss='mse', optimizer='adam')
    #model.compile(loss='mse', optimizer='adadelta')
    history = model.fit_generator(gen.generar(), steps_per_epoch=10, epochs=80, verbose=1)
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
