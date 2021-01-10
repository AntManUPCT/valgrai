#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:22:25 2020

@author: manuel
"""

import random

MAZO = [str(a) + str(b) for a in range(7) for b in range(a, 7)]
MLEN = len(MAZO)
CODG = {f: i for i, f in enumerate(MAZO)}


def codes(fichas):
    return [i for i in map(lambda f: CODG[f], fichas)]


def swap(ficha):
    return ficha[1] + ficha[0]


def match(ficha, num):
    return num in ficha


def shuffle():
    result = MAZO.copy()
    random.shuffle(result)
    return result


def take(fichas, num):
    taken = fichas[0:num]
    del fichas[0:num]
    return taken


def score_ficha(ficha):
    return int(ficha[0]) + int(ficha[1])


def score_fichas(fichas):
    return sum(map(score_ficha, fichas))


PUNTOS = list(map(score_ficha, MAZO))
MAX_PUNTOS = score_fichas(MAZO)


def try_first(ficha, fichas):
    if len(fichas) == 0:
        return True
    return match(ficha, fichas[0])


def try_last(ficha, fichas):
    if len(fichas) == 0:
        return True
    return match(ficha, fichas[-1])


def put_first(ficha, fichas):
    if len(fichas) == 0:
        return ficha
    if ficha[0] == fichas[0]:
        ficha = swap(ficha)
    return ficha[0] + fichas


def put_last(ficha, fichas):
    if len(fichas) == 0:
        return ficha
    if ficha[-1] == fichas[-1]:
        ficha = swap(ficha)
    return fichas + ficha[-1]


def poner_ficha(mesa, lado, ficha):
    if lado == 'F':
        return put_first(ficha, mesa)
    elif lado == 'L':
        return put_last(ficha, mesa)


def played(j):
    return (j[0], MAZO[j[1]])


JUGADORES = 4
