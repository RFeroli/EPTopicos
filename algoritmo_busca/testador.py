from subprocess import call
from ast import literal_eval
import statistics

saida_estatisticas = '../estatisticas/saida_problema.txt'
f = open(saida_estatisticas, 'w')
f.close()

qtd_experimentos = 20
for i in range(qtd_experimentos):
    call(['python3', 'run.py'])
