import random
import numpy as np

MAZO=[str(a)+str(b) for a in range(7) for b in range(a, 7)]
MLEN=len(MAZO)
CODG={f:i for (f, i) in zip(MAZO, range(MLEN))}

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

MAX_PUNTOS = score_fichas(MAZO)

def rotate_right(v):
    rr = np.empty(v.shape, dtype=v.dtype)
    rr[0]  = v[-1]
    rr[1:] = v[0:-1]
    return rr

def rotate_left(v):
    rl = np.empty(v.shape, dtype=v.dtype)
    rl[-1] = v[0]
    rl[0:-1] = v[1:]
    return rl

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

class domino_cb:
    def __init__(self, elegir, puntos):
        self.elegir = elegir
        self.puntos = puntos

JUGADORES = 4
IMG_ALTO = 50
IMG_ANCHO = MLEN + MLEN + 3
LADO_F = MLEN + MLEN
LADO_L = LADO_F + 1
JUGADO = LADO_L + 1

class Jugador:
    
    def __init__(self, turno, fichas, jugado = np.zeros((IMG_ALTO, IMG_ANCHO), dtype='uint8')):
        self.fichas = fichas
        self.turno = turno % JUGADORES
        self.jugado = jugado

    def ficha(self, indx):
        return self.fichas[indx]

    def puntos(self):
        return score_fichas(self.fichas)

    def opciones(self, mesa):
        if len(mesa) == 0:
            return [('F', i) for i in range(len(self.fichas))]

        result=[]
        for i in range(len(self.fichas)):
            ficha = self.fichas[i]
            if try_first(ficha, mesa):
                result.append(('F', i))
            if try_last(ficha, mesa):
                result.append(('L', i))
        return result

    def jugar(self, lado, ficha, turno):
        # Esto se hace para todos los jugadores
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()
        code = CODG[ficha]
        jugado[turno, code] = 255
        if lado == 'F':
            jugado[turno, LADO_F]=255
        elif lado == 'L':
            jugado[turno, LADO_L]=255
        jugado[turno, JUGADO] = 255

        return Jugador(self.turno, fichas, jugado)

    def ficha_usada(self, indx, turno):
        # Esto es solo para el jugador que mueve ficha
        if self.turno == (turno % JUGADORES):
            self.fichas.pop(indx)
            for ficha in self.fichas:
                code = CODG[ficha]
                self.jugado[turno, MLEN + code] = 255

    def pasar(self, turno):
        fichas = self.fichas.copy()
        jugado = self.jugado.copy()
        jugado[turno, JUGADO] = 255
        # Esto es solo para el jugador que mueve ficha
        if self.turno == (turno % JUGADORES):
            for ficha in self.fichas:
                code = CODG[ficha]
                jugado[turno, MLEN + code] = 255
        
        return Jugador(self.turno, fichas, jugado)

    def fin(self):
        return len(self.fichas) == 0

def poner_ficha(mesa, lado, ficha):
    if lado == 'F':
        return put_first(ficha, mesa)
    elif lado == 'L':
        return put_last(ficha, mesa)

class Estado:
    '''
    El estado del juego viene determinado por las fichas que tiene
    cada jugador y la información de lo que han puesto los otros
    jugadores en las jugadas anteriores
    '''

    def __init__(self, jugadores, turno=0, pasan=0, mesa=''):
        self.jugadores = jugadores
        self.turno = turno
        self.pasan = pasan
        self.mesa = mesa

    def jugador(self):
        indx = self.turno % JUGADORES
        return self.jugadores[indx]

    def puntos(self):
        return [j.puntos() for j in self.jugadores]

    def opciones(self):
        return self.jugador().opciones(self.mesa)

    def jugar(self, jugada):
        ''' Devolver el nuevo estado '''
        lado = jugada[0]
        indx = jugada[1]
        ficha = self.jugador().ficha(indx)

        jugadores = [j.jugar(lado, ficha, self.turno) for j in self.jugadores]
        jugadores[self.turno % JUGADORES].ficha_usada(indx, self.turno)
        mesa = poner_ficha(self.mesa, lado, ficha)
        return Estado(jugadores, self.turno + 1, 0, mesa)

    def pasar(self):
        ''' Devolver el nuevo estado '''
        jugadores = [j.pasar(self.turno) for j in self.jugadores]
        return Estado(jugadores, self.turno + 1, self.pasan + 1, self.mesa)

    def fin_partida(self):
        return any(map(lambda j: j.fin(), self.jugadores))

def play(state, cb):
    '''Devuelve una lista de puntos conseguidos'''
    if state.pasan==4:
        puntos = state.puntos()
        # El callback es para notificar el estado y la recompensa
        cb.puntos(state, puntos)
        return puntos

    opciones = state.opciones()
    if len(opciones) > 0:
        jugada = cb.elegir(opciones)
        lado = jugada[0]
        ficha = state.jugador().ficha(jugada[1])
        
        new_state = state.jugar(jugada)

        if new_state.fin_partida():
            puntos = new_state.puntos()
            cb.puntos(new_state, puntos)
            return puntos
        else:
            puntos = play(new_state, cb)
            cb.puntos(state, puntos)
            return puntos
    else:
        new_state = state.pasar()
        puntos = play(new_state, cb)
        cb.puntos(state, puntos)
        return puntos

def play_game():
    
    cb = domino_cb(
        lambda o: o[0],
        lambda state, puntos: print(state.mesa, puntos)
        )

    mezcla = shuffle()
    j1 = Jugador(0, take(mezcla, 7))
    j2 = Jugador(1, take(mezcla, 7))
    j3 = Jugador(2, take(mezcla, 7))
    j4 = Jugador(3, take(mezcla, 7))

    print(j1.fichas)
    print(j2.fichas)
    print(j3.fichas)
    print(j4.fichas)

    state = Estado([j1, j2, j3,j4])
    print("Puntos antes:", state.puntos())
    
    puntos = play(state, cb)
    print("Puntos despues: ", puntos)
    
