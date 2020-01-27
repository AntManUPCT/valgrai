#!/usr/bin/env python3

import juego
import entrenar
import estrategia

import numpy as np

class verificador:

    def __init__(self, model):
        self.policy = estrategia.Estrategia(model)

    def eleccion(self, mesa, jugador, opciones, turno):
        # Ordenador contra tres humanos
        if jugador.turno == 0:
            values = self.policy.evaluar(jugador, opciones, turno)
            print('ORDENADOR --------------------------------')
            print('Mesa ...: ' + mesa) 
            print('Opciones: [', end='') 
            for i, (lado, index) in enumerate(opciones):
                ficha = jugador.ficha(index)
                print('({}/{} {}), '.format(i, lado, ficha), end='')
            print('')
            print('ValoresQ: ', values)
            return opciones[np.argmax(values)]
        else:
            values = self.policy.evaluar(jugador, opciones, turno)
            print('HUMANO {} ---------------------------------'.format(jugador.turno))
            print('Mesa ...: ' + mesa)
            print('Fichas..: ', jugador.fichas)
            for i, (lado, index) in enumerate(opciones):
                ficha = jugador.ficha(index)
                print('Opcion {}: {} {} ({})'.format(i, lado, ficha, values[i]))

            opcion = int(input('Opcion elegida: '))
            return opciones[opcion]

    def puntuacion(self, state, puntos):
        print('Puntos: ', puntos, 'Mesa: ', state.mesa)

    def inipartida(self, sale):
        print('Sale:' , sale)

    def finpartida(self, puntos):
        print('Puntos : ', puntos)
        print('Ganador:', np.argmin(puntos))

    def funcion_Q(self):
        cb = juego.domino_cb(self.eleccion, self.puntuacion, self.finpartida)
        juego.domino(cb)
        

if __name__ == '__main__':

    # Cargar el modelo entrenado
    model = entrenar.modelo()
    model.load_weights('domino.hdf5')

    # Crear el verificador del modelo
    verif = verificador(model)

    # Mostrar la evaluacion del la funcion Q tras el entrenamiento
    verif.funcion_Q()
    
