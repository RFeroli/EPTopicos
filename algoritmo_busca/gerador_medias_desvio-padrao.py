from ast import literal_eval
import statistics

saida_estatisticas = '../estatisticas/saida_problema.txt'
linhas = open(saida_estatisticas, 'r').readlines()

print('-----------------\n\tApós {} iteraçoes\n-----------------\n'.format(len(linhas)))
#
nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = ['Problema do robo: 2 caixas', 'Problema do robo: 3 caixas', 'Problema do robo: 4 caixas',
                'Problema do robo: 5 caixas', 'Problema do robo: 6 caixas', 'Problema do robo: 7 caixas',
                'Problema do robo: 8 caixas', 'Problema do robo: 9 caixas', 'Problema do robo: 10 caixas',
             'Problema TyreWorld']
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['um', 'soma', 'max',"FF"]

for problema in problemas:
    print(problema + '\n')
    for heuristica in heuristicas:
        tempo, visitados, com_repeticoes, sem_repeticoes, taxa_ramificacao, comprimento_plano = [], [], [], [], [], []
        for rodada in linhas:
            dict = literal_eval(rodada)
            l = dict[problema][heuristica]
            tempo.append(l[0])
            visitados.append(l[1])
            com_repeticoes.append(l[2])
            sem_repeticoes.append(l[3])
            taxa_ramificacao.append(l[4])
            comprimento_plano.append(l[5])
        print('\tPara a heuristica {}, temos respectivamente média e desvio padrao de:'.format(nome_heuristica[heuristica]))
        print('\t\tExecuçao(ms)\t{}\t{} \n\t\tNós visitados\t{}\t{} \n\t\tGerados (com repetiçao)\t{}\t{}'.format(
                round(statistics.mean(tempo),2),round(statistics.stdev(tempo),2), round(statistics.mean(visitados),2),
                round(statistics.stdev(visitados), 2), round(statistics.mean(com_repeticoes),2), round(statistics.stdev(com_repeticoes),2)
            ))

        print('\t\tGerados (sem repetiçao)\t{}\t{} \n\t\tTaxa de Ramificaçao\t{}\t{} \n\t\tComprimento Plano\t{}\t{}'.format(
                round(statistics.mean(sem_repeticoes), 2), round(statistics.stdev(sem_repeticoes), 2), round(statistics.mean(taxa_ramificacao), 2),
            round(statistics.stdev(taxa_ramificacao), 2), round(statistics.mean(comprimento_plano), 2), round(statistics.stdev(comprimento_plano), 2)))
        print('\n')
