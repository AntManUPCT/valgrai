#!/usr/bin/env python3
import domino
import juego
from jugador import IMG_ITEMS 
import estrategia

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
#from PIL import Image, ImageDraw

def explog(x):
    return (np.exp(x) - 1)*(x <= 0) + np.log(x + 1)*(x > 0)

def loglog(x):
    return -np.log(1 - x)*(x <= 0) + np.log(x + 1)*(x > 0)

def expexp(x):
    return (np.exp(x) - 1)*(x <= 0) + (1 - np.exp(-x)*(x > 0))

def loglin(x):
    return -np.log(1 - x)*(x <= 0) + x*(x > 0)

# La funcion choice() seleccionará una accion usando el modelo provisional
# La funcion puntuar() entrenara el modelo con las recompensas obtenidas

class generador:

    def __init__(self, model, bs, gamma=1.0):
        self.model = model
        self.policy = estrategia.Estrategia(model)
        self.bs = bs
        self.gamma = gamma
        self.maxsize = 4*bs
        self.offset = 0
        self.x_train = np.zeros((self.maxsize, IMG_ITEMS), dtype='float32')
        self.y_train = np.zeros((self.maxsize, 1), dtype='float32')
        self.lote = 0
        self.indx = 0
        self.dc = 0
        self.cb = juego.domino_cb(self.eleccion, self.recompensa)

    def aleatoria(self, jugadr, opciones, turno):
        return opciones[0]

    def eleccion(self, jugadr, opciones, turno):
        return self.policy.elegir(jugadr, opciones, turno)

    def recompensa(self, state, puntos):
        indx = state.turno % domino.JUGADORES # Indice del jugador segun su turno
        self.x_train[self.indx, :] = state.jugadores[indx].jugado.reshape((IMG_ITEMS,))
        self.y_train[self.indx, :] = puntos[indx]
        self.indx = (self.indx + 1) % self.maxsize # Indice en el buffer circular
        self.dc = self.dc + 1 # data counter

    def generar(self):
        while True:
            while self.dc >= self.bs:
                self.lote = self.lote + 1
                first = self.offset
                last = first + self.bs
                self.offset = last % self.maxsize
                self.dc = self.dc - self.bs
                yield self.x_train[first:last, :], self.y_train[first:last, :]

            while self.dc < self.bs:
                mezcla = juego.shuffle()
                j1 = juego.Jugador(0, juego.take(mezcla, 7))
                j2 = juego.Jugador(1, juego.take(mezcla, 7))
                j3 = juego.Jugador(2, juego.take(mezcla, 7))
                j4 = juego.Jugador(3, juego.take(mezcla, 7))

                state = juego.Estado([j1, j2, j3,j4])

                juego.play(state, self.cb, self.gamma)

def modelo():
    model = Sequential()
    model.add(Dense(50, activation='relu', input_shape=(IMG_ITEMS,)))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    print(model.summary(90))
    return model
    
def entrenar():
    model = modelo()
    gen = generador(model, 2000, 0.95)
    model.compile(loss='mean_squared_error', optimizer='sgd')
    model.fit_generator(gen.generar(), steps_per_epoch=50, epochs=10, verbose=1)

def probar():
    model = modelo()
    gen = generador(model, 100)
    gen.generar()
    
if __name__ == "__main__":
    
    entrenar()
    #probar()
    
