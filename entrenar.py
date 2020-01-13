#!/usr/bin/env python3
import juego
from jugador import IMG_ALTO, IMG_ANCHO

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

IMG_ITEMS = IMG_ALTO*IMG_ANCHO

def eleccion(opciones, turno):
    return opciones[0]

def recompensa(state, puntos):
    indx = state.turno % juego.JUGADORES    
    x_train = state.jugadores[indx].jugado.reshape((juego.IMG_ITEMS))
    y_train = puntos[indx]
    yield x_train, y_train

def generador():
    while True:
        mezcla = juego.shuffle()
        j1 = juego.Jugador(0, juego.take(mezcla, 7))
        j2 = juego.Jugador(1, juego.take(mezcla, 7))
        j3 = juego.Jugador(2, juego.take(mezcla, 7))
        j4 = juego.Jugador(3, juego.take(mezcla, 7))

        state = juego.Estado([j1, j2, j3,j4])
        cb = juego.domino_cb(eleccion, recompensa)

        juego.play(state, cb)
        #puntos = juego.play(state, cb)
        #print(puntos)

def entrenar():

    model = Sequential()

    model.add(Dense(100, activation='relu', input_shape=(IMG_ITEMS,)))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))

    print(model.summary(90))

    model.compile(loss='mean_squared_error', optimizer='sgd')
    model.fit_generator(generador(), steps_per_epoch=30, epochs=10, verbose=1)

if __name__ == "__main__":
    
    entrenar()
    
    
