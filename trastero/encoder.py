#!/usr/bin/env python3
from juego import *

import gc
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from PIL import Image, ImageDraw

def explog(x):
    return (np.exp(x) - 1)*(x <= 0) + np.log(x + 1)*(x > 0)

def loglog(x):
    return -np.log(1 - x)*(x <= 0) + np.log(x + 1)*(x > 0)

def expexp(x):
    return (np.exp(x) - 1)*(x <= 0) + (1 - np.exp(-x)*(x > 0))

def loglin(x):
    return -np.log(1 - x)*(x <= 0) + x*(x > 0)

CODG={f:i for (f, i) in zip(MAZO, range(MLEN))}

NFEAT = MLEN + 2

def elegir_ficha(opciones):
    return random.choice(opciones)

class codificador:

    def __init__(self):
        self.seq = []
        self.ptos = (0,0,0,0)
        self.row = 0

    def poner_ficha(self, lado, ficha, img):
        x = CODG[ficha]
        img[self.row, x] = 255
        img[self.row, MLEN + (lado == 'L')] = 255
        img[self.row, MLEN + 2] = 255
        self.row += 1

    def pasar_turno(self, img):
        img[self.row, MLEN + 2] = 255
        self.row += 1

    def fin_juego(self, j1, j2, j3, j4, turno):
        index = [turno, (turno+1)%4, (turno+2)%4, (turno+3)%4]
        queda = [j1, j2, j3, j4]
        for (i, q) in zip(index, queda):
            self.ptos[i] = score_fichas(q)
        
    def jugar(self):
        self.seq = []
        self.ptos = [0,0,0,0]
        
        mezcla = shuffle()
        j1 = take(mezcla, 7)
        j2 = take(mezcla, 7)
        j3 = take(mezcla, 7)
        j4 = take(mezcla, 7)

        cb = domino_cb(
            lambda o: random.choice(o),
            lambda l, f: self.poner_ficha(l, f),
            lambda: self.pasar_turno(),
            lambda j1,j2,j3,j4,t: self.fin_juego(j1, j2, j3, j4, t)
            )

        play('', j1, j2, j3, j4, 0, 0, cb)

    def generar(self, partidas, file):
        data_file = open(file+'_x.csv', 'w')
        label_file = open(file+'_y.csv', 'w')
        data_writer = csv.writer(data_file)
        label_writer = csv.writer(label_file)
        
        for p in range(partidas):
            self.jugar()
            data_writer.writerow(self.seq)
            label_writer.writerow(self.ptos)

        data_file.close()
        label_file.close()

IMG_ALTO = 50
IMG_ANCHO = 1 + MLEN + 2

class entrenador_imagenes:

    def __init__(self, csvfile, samples):
        self.images = np.zeros((samples, IMG_ALTO, IMG_ANCHO), dtype='uint8')
        with open(csvfile) as file:
            cont = 0
            for line in file.readlines():
                self.encode_image(eval('['+line[0:-1]+']'), self.images[cont])
                cont += 1
                if cont % 1000 == 0:
                    print(cont, end='\r')
                if cont == samples:
                    break

    def encode_image(self, seq, img):
        row = 0
        for x in seq:
            if x>=0:
                img[row, x % MLEN] = 255
                if x < MLEN:
                    img[row, MLEN] = 255
                else:
                    img[row, MLEN + 1] = 255
            img[row, MLEN + 2] = 255
            row += 1

if __name__ == "__main__":
    import sys

    coder = codificador():
