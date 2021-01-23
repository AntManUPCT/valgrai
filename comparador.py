#!/usr/bin/env python3

import juego
import entrenar
import policy
import minimax

import numpy as np
import argparse


class comparador:

    def __init__(self, policies):
        self.policies = policies
        self.contadores = np.zeros((4,), dtype='int32')

    def eleccion(self, mesa, jugador, opciones):
        return self.policies[jugador.turno].elegir(mesa, jugador, opciones)

    def finpartida(self, puntos):
        minpuntos = np.min(puntos)
        for i, p in enumerate(puntos):
            if p == minpuntos:
                self.contadores[i] += 1

    def jugar(self):
        cb = juego.domino_cb(
            self.eleccion,
            lambda state, puntos: None,
            self.finpartida,
            lambda state, jugada: None,
            lambda state: None
        )
        juego.domino(cb)


if __name__ == '__main__':

    def RandomPolicies():
        return [
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.RandomPolicy()
        ]

    def MaxValueVersusRandom():
        return [
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.MaxValuePolicy()
        ]

    def QFunctionVersusRandom(model):
        return [
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.QFunction(model)
        ]

    def MinMaxVersusRandom(model):
        return [
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            minimax.MiniMax(model)
        ]

    def NeuralNetsVersusRandom(model):
        return [
            policy.RandomPolicy(),
            policy.RandomPolicy(),
            policy.QFunction(model),
            minimax.MiniMax(model)
        ]

    def MaxValueVersusQFunction(model):
        return [
            policy.MaxValuePolicy(),
            policy.QFunction(model),
            policy.MaxValuePolicy(),
            policy.QFunction(model)
        ]

    def MaxValueVersusMinMax(model):
        return [
            policy.MaxValuePolicy(),
            minimax.MiniMax(model),
            policy.MaxValuePolicy(),
            minimax.MiniMax(model)
        ]

    def AllVersusAll(model):
        return [
            policy.QFunction(model),
            minimax.MiniMax(model),
            policy.MaxValuePolicy(),
            policy.RandomPolicy()
        ]

    parser = argparse.ArgumentParser(description='Seleccionar jugadores')
    parser.add_argument("-j", "--jugadores", help="Elegir el conjunto de jugadores")
    args = parser.parse_args()

    # Cargar el modelo entrenado
    model = entrenar.modelo()
    model.load_weights('domino.hdf5')

    # Crear el verificador del modelo
    if args.jugadores == '0':
        comp = comparador(RandomPolicies())
    elif args.jugadores == '1':
        comp = comparador(MaxValueVersusRandom())
    elif args.jugadores == '2':
        comp = comparador(QFunctionVersusRandom(model))
    elif args.jugadores == '3':
        comp = comparador(MinMaxVersusRandom(model))
    elif args.jugadores == '4':
        comp = comparador(NeuralNetsVersusRandom(model))
    elif args.jugadores == '5':
        comp = comparador(MaxValueVersusQFunction(model))
    elif args.jugadores == '6':
        comp = comparador(MaxValueVersusMinMax(model))
    else:
        comp = comparador(AllVersusAll(model))

    # A jugar todo el mundo
    for i in range(4000):
        comp.jugar()
        if i % 1000 == 0:
            print(i, comp.contadores, end='\r')

    print('Ganadas: ', comp.contadores)
    suma = sum(comp.contadores)
    ratios = np.round(np.array(comp.contadores) * 100.0 / suma, 1)
    print('Ratios.: ', ratios)
