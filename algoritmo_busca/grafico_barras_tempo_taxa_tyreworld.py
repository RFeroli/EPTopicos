import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from statistics import mean

objects = ['Retorna 1', 'Soma de níveis', 'Nível máximo', 'Fast Forward']
y_pos = np.arange(len(objects))

saida_estatisticas = '../estatisticas/saida_problema.txt'
linhas = open(saida_estatisticas, 'r').readlines()


nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema tyreworld
problema = ('tyreworld_domain.pddl', 'tyreworld_problem.pddl', 'Problema TyreWorld')

# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['um', 'soma', 'max',"FF"]

heuristica_medias = {}
for heuristica in heuristicas:
    tempo, visitados, com_repeticoes, sem_repeticoes, taxa_ramificacao, comprimento_plano = [], [], [], [], [], []
    for rodada in linhas:
        dict = literal_eval(rodada)
        l = dict[problema[2]][heuristica]
        tempo.append(l[0])
        # visitados.append(l[1])
        # com_repeticoes.append(l[2])
        # sem_repeticoes.append(l[3])
        taxa_ramificacao.append(l[4])
        # comprimento_plano.append(l[5])

    heuristica_medias[heuristica] = [round(mean(tempo), 2), round(mean(taxa_ramificacao),2)]

print(heuristica_medias)




# Consumo de tempo
performance = [heuristica_medias['um'][0], heuristica_medias['soma'][0],
             heuristica_medias['max'][0], heuristica_medias['FF'][0]]


plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Tempo (ms)')
plt.title('Consumo médio de tempo (ms) de cada heurística para o problema Tyre World')

plt.show()

# Taxa de ramificaçao
performance = [heuristica_medias['um'][1], heuristica_medias['soma'][1],
             heuristica_medias['max'][1], heuristica_medias['FF'][1]]


plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('nós')
plt.title('Taxa de ramificaçao média de cada heurística para o problema Tyre World')

plt.show()