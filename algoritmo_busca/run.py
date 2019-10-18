from subprocess import call
import time

saida_estatisticas = '../estatisticas/saida_problema.txt'
f = open(saida_estatisticas, 'w')
f.close()

qtd_experimentos = 20
it = time.time()
for i in range(qtd_experimentos):
    call(['python3', 'ciclo.py'])
print('Demorou {} ms'.format(time.time()-it))