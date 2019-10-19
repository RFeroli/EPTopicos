from subprocess import call
import time

saida_estatisticas = '../estatisticas/saida_problema.txt'
f = open(saida_estatisticas, 'w')
f.close()

qtd_experimentos = 100
print('comecou')
for i in range(qtd_experimentos):
    it = time.time()
    call(['python3', 'ciclo.py'])
    print('Demorou {} segs'.format(time.time()-it))