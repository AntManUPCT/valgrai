import numpy as np

def explog(x):
    return (np.exp(x) - 1)*(x <= 0) + np.log(x + 1)*(x > 0)

def loglog(x):
    return -np.log(1 - x)*(x <= 0) + np.log(x + 1)*(x > 0)

def expexp(x):
    return (np.exp(x) - 1)*(x <= 0) + (1 - np.exp(-x)*(x > 0))

def loglin(x):
    return -np.log(1 - x)*(x <= 0) + x*(x > 0)

CODG={f:i for (f, i) in zip(MAZO, range(MLEN))}
#code = CODG[ficha]

def poner_ficha(lado, ficha):
    codigo = CODG[ficha]
    if lado == 'L':
        codigo = MLEN + codigo
    print(codigo)

def pasar_turno():
    codigo = 0
    print(codigo)

def fin_juego(j1, j2, j3, j4, turno):
    result = np.zeros(4)
    index = [turno, (turno+1)%4, (turno+2)%4, (turno+3)%4]
    queda = [j1, j2, j3, j4]
    for (i, q) in zip(index, queda):
        result[i] = score_fichas(q)
    for i in range(4):
        print('J{} Puntos: {}'.format(i, result[i]))
    

def entrenar_autoencoder():
    mezcla = shuffle()
    j1 = take(mezcla, 7)
    j2 = take(mezcla, 7)
    j3 = take(mezcla, 7)
    j4 = take(mezcla, 7)

    print(j1, j2, j3, j4, sep='\n')

    cb = domino_cb(
        lambda l, f: poner_ficha(l, f),
        lambda: pasar_turno(),
        lambda j1,j2,j3,j4,t: fin_juego(j1, j2, j3, j4, t)
        )

    play('', j1, j2, j3, j4, 0, 0, cb)



                                       
