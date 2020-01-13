#!/usr/bin/env python3
import csv

class preprocess:

    def __init__(self, filein):
        self.maxlen = 0
        self.data = []
        with open(filein) as file:
            for line in file.readlines():
                seq = eval('['+line[0:-1]+']')
                self.maxlen = max(self.maxlen, len(seq))
                self.data.append(seq)
    
    def extrae_secuencias(self, lenseq, fileout):
        with open(fileout, 'w') as file:
            writer = csv.writer(file)
            for seq in self.data:
                if  len(seq) < lenseq:
                    continue
                writer.writerow(seq[0:lenseq])
            
    def separa_secuencias(self, fileout):
        for seqlen in range(1, self.maxlen+1):
            outname = '{}_{:02}.csv'.format(fileout, seqlen)
            print('Generando: ' + outname)
            self.extrae_secuencias(seqlen, outname)

if __name__ == '__main__':
    import sys    
    prepro = preprocess(sys.argv[1])
    prepro.separa_secuencias(sys.argv[2])
