#!/usr/bin/env python3

from domino import MAZO
import juego
import entrenar
import policy
from resumido import Resumido
import numpy as np


class verificador:

    def __init__(self, model, bdmental):
        self.policy = policy.QFunction(model)
        self.bdmental = bdmental

    def eleccion(self, mesa, jugador, opciones):
        # Ordenador contra tres humanos
        if jugador.turno == 0:
            print('ORDENADOR --------------------------------')
            print('Mesa ...: ' + mesa)
            opcion = self.policy.elegir(mesa, jugador, opciones)
            print('Juega ..: ', opcion)
            return opcion
        else:
            print('HUMANO {} ---------------------------------'.format(jugador.turno))
            print('Mesa ...: ' + mesa)
            print('Fichas..: ', jugador.fichas)
            print('Opciones: ', opciones)

            opcion = int(input('Opcion elegida: '))
            return opciones[opcion]

    def puntuacion(self, state, puntos):
        print('Puntos: ', puntos, 'Mesa: ', state.mesa)

    def finpartida(self, puntos):
        print('Puntos : ', puntos)
        print('Ganador:', np.argmin(puntos))

    def funcion_Q(self):
        cb = juego.domino_cb(
            self.eleccion,
            self.puntuacion,
            self.finpartida,
            lambda state, jugada: None,
            lambda state: None
        )
        juego.domino(cb, bdmental)


if __name__ == '__main__':

    # Defnir la BD mental del jugador
    bdmental = Resumido

    # Cargar el modelo entrenado
    model = entrenar.modelo(bdmental.num_features())
    model.load_weights('domino.hdf5')

    # Crear el verificador del modelo
    verif = verificador(model, bdmental)

    # Mostrar la evaluacion del la funcion Q tras el entrenamiento
    verif.funcion_Q()
