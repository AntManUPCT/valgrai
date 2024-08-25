#!/usr/bin/env python3

import juego
import entrenar
import entrenar_transfo
import policy
from bdmental import BDMental
from resumido import Resumido
from textual import Textual

from domino import WORDS

import tensorflow as tf
import numpy as np
import argparse


class comparador:

    def __init__(self, config):
        self.policies = config["policies"]
        self.mentaldb = config["mentaldb"]
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
        juego.domino(cb, self.mentaldb)


if __name__ == '__main__':

    def crear_tokenizador():
        palabras = [' '.join(WORDS)]
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=50) # len(WORDS)+1)
        tokenizer.fit_on_texts(palabras)
        return tokenizer

    def AllVersusAll(model_PMC, model_Transfo):
        return {
            "policies" : [
                policy.RandomPolicy(),
                policy.MaxValuePolicy(),
                policy.QFunction(model_PMC),
                policy.Transfo_QFunction(model_Transfo, crear_tokenizador()),
            ],
            "mentaldb" : [
                BDMental,
                BDMental,
                Resumido,
                Textual
            ]
        }

    parser = argparse.ArgumentParser(description='Seleccionar jugadores')
    parser.add_argument("-j", "--jugadores", help="Elegir el conjunto de jugadores")
    args = parser.parse_args()

    # Cargar el modelo entrenado
    # modelo basado en Perceptron Multi Capa
    model_PMC = entrenar.modelo(Resumido.num_features())
    model_PMC.load_weights(entrenar.fichero_pesos)

    # modelo basado en un Transformador
    model_Transfo = entrenar_transfo.modelo(False)
    model_Transfo.load_weights(entrenar_transfo.fichero_pesos)

    # Crear el verificador del modelo
    comp = comparador(AllVersusAll(model_PMC, model_Transfo))

    # A jugar todo el mundo
    for i in range(4000):
        comp.jugar()
        if i % 100 == 0:
            print(i, comp.contadores, end='\r')

    print('Ganadas: ', comp.contadores)
    suma = sum(comp.contadores)
    ratios = np.round(np.array(comp.contadores) * 100.0 / suma, 1)
    print('Ratios.: ', ratios)
