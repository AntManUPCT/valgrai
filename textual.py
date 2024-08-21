#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Ago 213:29:50 2024

@author: antonio manuel
"""

from bdmental import BDMental
from domino import MLEN, CODG, JUGADORES
import numpy as np

"""
El estado de cada jugador esta compuesto por:
  1. La lista de jugadas anteriores
  2. Las fichas que le quedan

"""

class Textual(BDMental):

    @classmethod
    def num_features(cls):
        return None

    def __init__(self, clon=None):
        self.jugado = []
        self.fichas = []
        if clon is not None:
            self.jugado = clon.jugado

    def init(self, fichas):
        self.fichas = fichas
        return None

    def copy(self):
        return Textual(self) # No crear, se le pasa un clon

    def ficha_puesta(self, ficha, lado, id_jugador):
        self.jugado.append(ficha)
        self.jugado.append(lado)

        return None

    def jugador_pasa(self, mesa, id_jugador):
        self.jugado.append('PASA')

    def get_features(self):
        prompt = self.jugado.copy()
        prompt.append('FICHAS')
        prompt += self.fichas
        return prompt
