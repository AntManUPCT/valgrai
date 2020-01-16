#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import juego
import jugador
from jugador import IMG_ITEMS 

import numpy as np

class Estrategia:

    def __init__(self, model):
        self. model = model

    def elegir(self, jugador, opciones, turno):
        ''' Elegir la mejor opcion para este jugador según el modelo '''
        if len(opciones) == 1:
            return opciones[0]
        
        values = np.empty((len(opciones),), dtype='float32')
        vindex = 0
        for (lado, index) in opciones:
            ficha = jugador.ficha(index)
            # Nuevo estado del jugador tras probar esta accion
            nj = jugador.jugar(lado, ficha, turno, index)
            x =  nj.jugado.reshape((1, IMG_ITEMS))
            y = self.model.predict(x)
            values[vindex] = y
            vindex += 1

        return opciones[np.argmin(values)]

        
