from subprocess import call


saida_estatisticas = '../estatisticas/saida_problema.txt'
f = open(saida_estatisticas, 'w')
f.close()

qtd_experimentos = 20
for i in range(qtd_experimentos):
    call(['python3', 'ciclo.py'])
