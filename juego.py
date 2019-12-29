import random

MAZO=[str(a)+str(b) for a in range(7) for b in range(a, 7)]
MLEN=len(MAZO)

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

def end_game(j1, j2, j3, j4, turno):
    print('----- Fin juego -----')
    index = [turno, (turno+1)%4, (turno+2)%4, (turno+3)%4]
    queda = [j1, j2, j3, j4]
    for (i, q) in zip(index, queda):
        print('J{} Puntos: {} {}'.format(i, score_fichas(q), repr(q)))

def calcular_opciones(mesa, fichas):
    result=[]
    for i in range(len(fichas)):
        ficha = fichas[i]
        if try_first(ficha, mesa):
            result.append(('F', i))
        if try_last(ficha, mesa):
            result.append(('L', i))
    return result

class domino_cb:
    def __init__(self, poner, pasar, fin):
        self.poner = poner
        self.pasar = pasar
        self.fin = fin

def play(mesa, j1, j2, j3, j4, turno, pasan, cb):
    if pasan==4:
        cb.fin(j1, j2, j3, j4, turno)
        return

    siguiente = (turno + 1) % 4

    opciones = calcular_opciones(mesa, j1)
    if len(opciones) > 0:
        jugada = random.choice(opciones)
        l = jugada[0]
        i = jugada[1]
        ficha = j1[i]
        cb.poner(l, ficha)

        if l == 'F':
            mesa = put_first(ficha, mesa)
            del j1[i]
            if len(j1) > 0:
                play(mesa, j2, j3, j4, j1, siguiente, 0, cb)
            else:
                cb.fin(j1, j2, j3, j4, turno)
            return
        if l == 'L':
            mesa = put_last(ficha, mesa)
            del j1[i]
            if len(j1) > 0:
                play(mesa, j2, j3, j4, j1, siguiente, 0, cb)
            else:
                cb.fin(j1, j2, j3, j4, turno)
            return
    else:
        cb.pasar()
        play(mesa, j2, j3, j4, j1, siguiente, pasan+1, cb)

def play_game():
    mezcla = shuffle()
    j1 = take(mezcla, 7)
    j2 = take(mezcla, 7)
    j3 = take(mezcla, 7)
    j4 = take(mezcla, 7)

    print(j1, j2, j3, j4, sep='\n')

    cb = domino_cb(
        lambda l, f: print(l, f),
        lambda: print('Paso'),
        lambda j1,j2,j3,j4,t: end_game(j1, j2, j3, j4, t)
        )

    play('', j1, j2, j3, j4, 0, 0, cb)
    
