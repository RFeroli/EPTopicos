from ast import literal_eval
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


saida_estatisticas = '../estatisticas/saida_problema.txt'
linhas = open(saida_estatisticas, 'r').readlines()


nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = [('tyreworld_domain.pddl', 'tyreworld_problem.pddl', 'Problema TyreWorld')]
# problemas = [('robot_domain.pddl', 'robot_problem.pddl', 'Problema do robo')]
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['um', 'soma', 'max',"FF"]
from statistics import mean

legenda = ['Visitados', 'gerados (cr)', 'gerados (sr)']

for problema in problemas:
    print(problema[2] + '\n')
    heuristica_medias = {}
    for heuristica in heuristicas:
        tempo, visitados, com_repeticoes, sem_repeticoes, taxa_ramificacao, comprimento_plano = [], [], [], [], [], []
        for rodada in linhas:
            dict = literal_eval(rodada)
            l = dict[problema[2]][heuristica]
            tempo.append(l[0])
            visitados.append(l[1])
            com_repeticoes.append(l[2])
            sem_repeticoes.append(l[3])
            taxa_ramificacao.append(l[4])
            comprimento_plano.append(l[5])

        heuristica_medias[heuristica] = [round(mean(visitados), 2), round(mean(com_repeticoes),2),
                                         round(mean(sem_repeticoes),2)]

    print(heuristica_medias)

    # labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    # men_means = [20, 34, 30, 35, 27]
    # women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(legenda))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 3*width/4, heuristica_medias['um'], width/2, label='Retorna 1', capsize=10)
    rects2 = ax.bar(x - width/4, heuristica_medias['soma'], width/2, label='Soma de Níveis')
    rects3 = ax.bar(x + width/4, heuristica_medias['max'], width/2, label='Nível Máximo')
    rects4 = ax.bar(x + 3*width/4, heuristica_medias['FF'], width/2, label='Fast Forward')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Nós')
    ax.set_title('Comparação de heurísticas ('+problema[2]+')')
    ax.set_xticks(x)
    ax.set_xticklabels(legenda)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)

    fig.tight_layout()

    plt.show()
