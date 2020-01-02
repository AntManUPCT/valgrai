#!/usr/bin/env python3
from juego import *

import gc
import csv
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed

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

class generador:

    def __init__(self):
        self.seq = []
        self.ptos = [0,0,0,0]
    
    def poner_ficha(self, lado, ficha):
        codigo = CODG[ficha]
        if lado == 'L':
            codigo = MLEN + codigo
        self.seq.append(codigo)

    def pasar_turno(self):
        codigo = -1
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

class entrenador:

    def __init__(self, csvfile):
        samples = []
        with open(csvfile) as file:
            cont = 1
            for line in file.readlines():
                samples.append(self.encode_sample(eval('['+line[0:-1]+']')))
                cont += 1
                if cont % 1000 == 0:
                    print(cont, end='\r')
                    gc.collect()

        self.data = np.array(samples)
        gc.collect()

    def encode_sample(self, seq):
        data = []
        for x in seq:
            if x<0:
                data.append(np.zeros(NFEAT))
            else:
                coded = keras.utils.to_categorical(x % MLEN, num_classes=NFEAT)
                if x < MLEN:
                    coded[MLEN]=1
                else:
                    coded[MLEN+1]=1
                data.append(coded)
        return data

    def entrenar(self):
        X = self.data
        samples, timesteps, n_features = X.shape

        # define model
        model = Sequential()
        model.add(LSTM(128, activation='relu', input_shape=(timesteps, n_features), return_sequences=True))
        model.add(LSTM(64, activation='relu', return_sequences=False))
        model.add(RepeatVector(timesteps))
        model.add(LSTM(64, activation='relu', return_sequences=True))
        model.add(LSTM(128, activation='relu', return_sequences=True))
        model.add(TimeDistributed(Dense(n_features)))
        model.compile(optimizer='adam', loss='mse')
        model.summary()

        # fit model
        model.fit(X, X, epochs=5, batch_size=100, verbose=1)
        
        # demonstrate reconstruction
        yhat = model.predict(X[0:1], verbose=0)
        print('---Predicted---')
        print(np.round(yhat, 1))
        print('---Actual---')
        print(np.round(X[0:1], 1))

if __name__ == "__main__":
    import sys
    
    #gen = generador()
    #gen.generar(int(sys.argv[1]), sys.argv[2])

    ent = entrenador(sys.argv[1])
    ent.entrenar()
