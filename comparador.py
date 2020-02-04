#!/usr/bin/env python3

import juego
import entrenar
import estrategia
from domino import score_ficha

import numpy as np
import random

class comparador:

    def __init__(self, model):
        self.policy = estrategia.Estrategia(model)
        self.contadores = np.zeros((4,), dtype='int32')
        self.salidas = np.zeros((4,), dtype='int32')

    def eleccion(self, mesa, jugador, opciones, jugada):
        # Ordenador contra tres jugadores aleatorios
        if jugador.turno == 0:
            return random.choice(opciones)
        
        elif jugador.turno == 1:
            return random.choice(opciones)
        
        elif jugador.turno == 2:
            values = list(map(lambda opcion: score_ficha(jugador.ficha(opcion[1])), opciones))
            return opciones[np.argmax(values)]
                          
        elif jugador.turno == 3:
            # ORDENADOR
            values = self.policy.evaluar(jugador, opciones, jugada)
            return opciones[np.argmax(values)]

    def puntuacion(self, state, puntos):
        #print('Puntos: ', puntos, 'Mesa: ', state.mesa)
        pass

    def inipartida(self, sale):
        self.salidas[sale] += 1

    def finpartida(self, puntos):
        minpuntos = np.min(puntos)
        for i,p in enumerate(puntos):
            if p == minpuntos:
                self.contadores[i] += 1

    def jugar(self):
        cb = juego.domino_cb(self.eleccion, self.puntuacion, self.inipartida, self.finpartida)
        juego.domino(cb)


if __name__ == '__main__':

    # Cargar el modelo entrenado
    model = entrenar.modelo()
    model.load_weights('domino.hdf5')

    # Crear el verificador del modelo
    comp = comparador(model)

    # Jugar contra otros tres jugadores
    for i in range(10000):
        comp.jugar()
        if i % 1000 == 0:
            print(i, comp.contadores, end='\r')

    print('Ganadas: ', comp.contadores)
    print('Salidas: ', comp.salidas)
    suma = sum(comp.contadores)
    ratios = np.round(np.array(comp.contadores) * 100.0 / suma, 1)
    print('Ratios.: ', ratios)
