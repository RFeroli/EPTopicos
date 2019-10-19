from algoritmo_busca.busca import Busca
from main.planejador import Estado, Planejador
from main.conversorPDDL import Conversor
import time

nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = [
             ('robot_domain.pddl', 'robot_problem_2b.pddl', 'Problema do robo: 2 caixas'),
              ('robot_domain.pddl', 'robot_problem_3b.pddl', 'Problema do robo: 3 caixas'),
              ('robot_domain.pddl', 'robot_problem_4b.pddl', 'Problema do robo: 4 caixas'),
              ('robot_domain.pddl', 'robot_problem_5b.pddl', 'Problema do robo: 5 caixas'),
              ('robot_domain.pddl', 'robot_problem_6b.pddl', 'Problema do robo: 6 caixas'),
              ('robot_domain.pddl', 'robot_problem_7b.pddl', 'Problema do robo: 7 caixas'),
             ('robot_domain.pddl', 'robot_problem_8b.pddl', 'Problema do robo: 8 caixas'),
             ('robot_domain.pddl', 'robot_problem_9b.pddl', 'Problema do robo: 9 caixas'),
             ('robot_domain.pddl', 'robot_problem_10b.pddl', 'Problema do robo: 10 caixas'),
              ('tyreworld_domain.pddl', 'tyreworld_problem.pddl', 'Problema TyreWorld')
            ]
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
# TODO incluir FF
heuristicas = ['um','max','FF','soma']

path = '../in/'
saida_estatisticas = '../estatisticas/saida_problema.txt'
saida_planos = '../estatisticas/saida_planos.txt'
estatisticas = {'Problema do robo: 2 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 3 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 4 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 5 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 6 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 7 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 8 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 9 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema do robo: 10 caixas':{'um':[], 'soma': [], 'max': [], 'FF':[]},
                'Problema TyreWorld': {'um':[], 'soma': [], 'max': [], 'FF':[]}}

f = open(saida_estatisticas, 'a+')
f_planos = open(saida_planos, 'a+')

escreve_planos = ''
for problema in problemas:
    print('\n\nTratando o {}'.format(problema[2]))
    escreve_planos+='\n\nTratando o {}'.format(problema[2])
    for heuristica in heuristicas:
        experimento = []
        print('\nHeuristica: {}'.format(nome_heuristica[heuristica]))
        escreve_planos+='\nHeuristica: {}'.format(nome_heuristica[heuristica])

        estado, meta, operacoes, argumentos  = Conversor(path + problema[0], path + problema[1]).get_planner_args()
        pl = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), heuristica)
        pl.nome_do_problema=problema[2]
        pl.gerar_grafico=False

        tempo_inicial = time.time()
        plano_estados, dicionario_expansao, contador_gerados = Busca().busca_a_estrela(pl)
        tempo_execucao = round((time.time()-tempo_inicial)*1000)

        print('O algoritmo levou {} milisegundos'.format(tempo_execucao))
        escreve_planos+='O algoritmo levou {} milisegundos'.format(tempo_execucao)
        experimento.append(tempo_execucao)

        print('No total {} nós foram visitados\nTivemos {} nós gerados com repeticçoes e {} sem repetiçoes\nE a taxa de ramificaçao foi de {} filhos por nó'.format(
            len(dicionario_expansao), sum(list(dicionario_expansao.values())), contador_gerados,
            round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2)))
        escreve_planos+='No total {} nós foram visitados\nTivemos {} nós gerados com repeticçoes e {} sem repetiçoes\nE a taxa de ramificaçao foi de {} filhos por nó'.format(
            len(dicionario_expansao), sum(list(dicionario_expansao.values())), contador_gerados,
            round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2))

        experimento.append(len(dicionario_expansao))
        experimento.append(sum(list(dicionario_expansao.values())))
        experimento.append(contador_gerados)
        experimento.append(round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2))
        experimento.append(len(plano_estados))

        print('O plano possui {} passos, os quais, a partir do estado inicial, sao:'.format(len(plano_estados)))
        escreve_planos+='O plano possui {} passos, os quais, a partir do estado inicial, sao:'.format(len(plano_estados))
        for nc, i in zip(plano_estados, range(1, len(plano_estados)+1)):
            escreve_planos+= '{}: '.format(i)
            escreve_planos+= '\t Aplicando a açao {}, gera-se o estado'.format(str(nc.operacao))
            escreve_planos+= '\t\t' + str(nc.dict)+'\n'

            print('{}: '.format(i))
            print('\t Aplicando a açao {}, gera-se o estado'.format(str(nc.operacao)))
            print('\t\t' + str(nc.dict)+'\n')

        estatisticas[problema[2]][heuristica] = experimento
    f_planos.write(escreve_planos)

f.write(str(estatisticas)+'\n')
f.close()
f_planos.close()