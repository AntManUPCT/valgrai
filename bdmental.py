#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Ago 20 22:49:50 2024

@author: antonio manuel
"""

class BDMental:
    """
    Representa la Base de Datos mental de cada jugador.
    Contiene la información que cada jugador mantiene en su memoria
    sobre las acciones realizadas por todos los jugadores
    """

    @classmethod
    def num_features(cls):
        """Devuelve la dimension del vector de caracteristicas"""
        pass

    def init(self, fichas):
        """Inicializa la BD con las fichas del jugador"""
        pass

    def copy(self):
        """Clona la base de datos"""
        pass

    def ficha_puesta(self, ficha, lado, jugador):
        """Actualiza la BD con la nueva ficha colocada"""
        pass

    def jugador_pasa(self, mesa, jugador):
        """Actualiza la BD con la nueva información"""
        pass

    def get_features(self):
        """Devuelve el vector de caracteristicas"""
        pass
