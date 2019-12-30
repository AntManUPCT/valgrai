#!/usr/bin/env python3
from juego import *
import csv
import numpy as np
import keras

def explog(x):
    return (np.exp(x) - 1)*(x <= 0) + np.log(x + 1)*(x > 0)

def loglog(x):
    return -np.log(1 - x)*(x <= 0) + np.log(x + 1)*(x > 0)

def expexp(x):
    return (np.exp(x) - 1)*(x <= 0) + (1 - np.exp(-x)*(x > 0))

def loglin(x):
    return -np.log(1 - x)*(x <= 0) + x*(x > 0)

CODG={f:i for (f, i) in zip(MAZO, range(MLEN))}
NCLS=2*MLEN

def elegir_ficha(opciones):
    return random.choice(opciones)

class entrenador:

    def __init__(self):
        self.seq = []
        self.ptos = [0,0,0,0]
    
    def poner_ficha(self, lado, ficha):
        codigo = CODG[ficha]
        if lado == 'L':
            codigo = MLEN + codigo
        #self.seq.append(keras.utils.to_categorical(codigo, num_classes=NCLS))
        self.seq.append(codigo)

    def pasar_turno(self):
        codigo = -1
        #self.seq.append(np.zeros(NCLS))
        self.seq.append(codigo)

    def fin_juego(self, j1, j2, j3, j4, turno):
        result = np.zeros(4)
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

if __name__ == "__main__":
    import sys
    
    gen = entrenador()
    gen.generar(int(sys.argv[1]), sys.argv[2]) 
