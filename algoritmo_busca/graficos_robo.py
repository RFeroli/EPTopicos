from ast import literal_eval


import matplotlib
import matplotlib.pyplot as plt
import numpy as np


saida_estatisticas = '../estatisticas/saida_problema.txt'
linhas = open(saida_estatisticas, 'r').readlines()

linhas = [literal_eval(l) for l in linhas]

nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = ['Problema do robo: 2 caixas', 'Problema do robo: 3 caixas', 'Problema do robo: 4 caixas']
    # ,
    #          'Problema do robo: 5 caixas', 'Problema do robo: 6 caixas', 'Problema do robo: 7 caixas'
    #          'Problema do robo: 9 caixas', 'Problema do robo: 8 caixas', 'Problema do robo: 10 caixas']
# problemas = [('robot_domain.pddl', 'robot_problem.pddl', 'Problema do robo')]
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['um', 'soma', 'max',"FF"]
from statistics import mean



def plota_grafico(indice, label1, label2):
    n_caixas = [2, 3, 4]

    valores_heuristicas = {}
    for i in heuristicas:
        valores_heuristicas[i] = []

    for heuristica in heuristicas:
        for problema in problemas:
            print(problema + '\n')
            lista = []
            for rodada in linhas:
                # print(rodada)
                l = rodada[problema][heuristica]
                lista.append(l[indice])

            valores_heuristicas[heuristica].append(mean(lista))
        # heuristica_medias[heuristica] = [mean(visitados), mean(com_repeticoes), mean(sem_repeticoes)]

    # print(valores_heuristicas)

    plt.plot(n_caixas, valores_heuristicas['um'], color='green', label='Retorna 1')
    plt.plot(n_caixas, valores_heuristicas['soma'], color='orange', label='Soma de Níveis')
    plt.plot(n_caixas, valores_heuristicas['max'], color='red', label='Nível Máximo')
    plt.plot(n_caixas, valores_heuristicas['FF'], color='gray', label='Fast Forward')
    plt.xlabel('Número de caixas')
    plt.ylabel(label1)
    plt.title(label2)
    plt.legend()
    plt.show()



plota_grafico(0, 'tempo (ms)', 'Tempo em ms para as quatro heurísticas.')
plota_grafico(1, 'nós', 'Número de nós expandidos')
plota_grafico(2, 'nós', 'Nós criados com repetiçao')
plota_grafico(3, 'nós', 'Nós criados sem repetiçao')
plota_grafico(4, 'nós', 'Taxa de ramificaçao')
