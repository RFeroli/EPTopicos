from algoritmo_busca.busca import Busca
from main.planejador import Estado, Planejador
from main.conversorPDDL import Conversor
import time
import ast
import statistics
import random
import sys
# import copy
# def _gere_hash(o):
#     if isinstance(o, (set, tuple, list)):
#         return tuple([_gere_hash(e) for e in o])
#
#     elif not isinstance(o, dict):
#         return hash(o)
#
#     nova_estrutura = copy.deepcopy(o)
#     for k, v in nova_estrutura.items():
#         nova_estrutura[k] = _gere_hash(v)
#
#     return hash(tuple(frozenset(sorted(nova_estrutura.items()))))
#
# print(_gere_hash( {'operacao':{'move': ['room1', 'room2']}, 'nivel':2 } ))

# exit()


# estado = {'box-at': {('box1', 'room1'), ('box2', 'room1')},
#           'robot-at': {('room1',)},
#           # 'free': {('right',), ('left',)}}
#             'free': {('right',)}}
#
# meta = {'box-at': {('box1', 'room2'), ('box2', 'room2')}}
#
#
# # variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
# operacoes = {
#              'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
#                        {'free': [['?y']], 'robot-at':[['?w']], 'box-at': [['?x', '?w']]},
#                        {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],
#
#              'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': [['?x', '?y']], 'robot-at':[['?w']]},
#                         {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
#                         ],
#             'move':[['?x', '?y'], ['room', 'room'], {'robot-at':[['?x']]}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}
#
#
# argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2'}, 'arm': {'right'}}
#

#
# estado = {'in': {('jack', 'boot'), ('pump', 'boot'), ('wrench', 'boot'), ('r1', 'boot')},
#           'on': {('w1', 'the-hub1')},
#           'on-ground': {('the-hub1',)},
#           'unlocked': {('boot',)},
#           'closed': {('boot',)},
#           'intact': {('r1',)},
#           'not-inflated': {('r1',)},
#           'tight': {('nuts1', 'the-hub1')},
#           'fastened': {('the-hub1',)}
#           }
#
#
#
# meta = {    'in': {('w1', 'boot'), ('pump', 'boot'), ('wrench', 'boot'), ('jack', 'boot')},
#             'closed': {('boot',)},
#             'inflated': {('r1',)},
#             'tight': {('nuts1', 'the-hub1')},
#             'on':{('r1', 'the-hub1')}
#         }
#
#
# # variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
# operacoes = {
#
# 'close':[['?x'], ['container'], {'open':[['?x']]}, {'closed':('?x', )}, {'open':('?x', )}],
# 'open':[['?x'], ['container'], {'unlocked':[['?x']], 'closed':[['?x']]}, {'open':('?x', )}, {'closed':('?x', )}],
# 'inflate': [['?x'], ['wheel'],
#              {'not-inflated': [['?x']], 'intact': [['?x']], 'have': [['pump']]},
#              {'inflated': ('?x',)}, {'not-inflated': ('?x', )}
#              ],
#
#
#
# 'put-on-wheel': [['?x', '?y'], ['wheel', 'hub'],
#              {'not-on-ground': [['?y']], 'unfastened': [['?y']], 'have': [['?x']], 'free': [['?y']]},
#              {'on': ('?x', '?y')}, {'have': ('?x', ), 'free': ('?y',)}
#              ],
#
#
#
# 'remove-wheel': [['?x', '?y'], ['wheel', 'hub'],
#              {'not-on-ground': [['?y']], 'unfastened': [['?y']], 'on': [['?x', '?y']]},
#              {'have': ('?x', ), 'free': ('?y',)}, {'on': ('?x', '?y')}
#              ],
#
#
#             'do-up': [['?x', '?y'], ['nut', 'hub'],
#              {'not-on-ground': [['?y']], 'unfastened': [['?y']], 'have': [['wrench'], ['?x']]},
#              {'loose': ('?x', '?y'), 'fastened': ('?y',)}, {'unfastened': ('?y',), 'have': ('?x',)}
#              ],
#             'undo': [['?x', '?y'], ['nut', 'hub'],
#                      {'not-on-ground': [['?y']], 'fastened': [['?y']], 'loose': [['?x', '?y']], 'have': [['wrench']]},
#                 {'have': ('?x', ), 'unfastened': ('?y', )}, {'fastened': ('?y',), 'loose': ('?x', '?y')}
#                 ],
#
#
#             'jack-down': [['?y'], ['hub'], {'not-on-ground': [['?y']]},
#                 {'on-ground': ('?y',), 'have': ('jack',)}, {'not-on-ground': ('?y',)}
#                 ],
#
#
#             'jack-up': [['?y'], ['hub'], {'have': [['jack']], 'on-ground': [['?y']]},
#                 {'not-on-ground': ('?y',)}, {'on-ground': ('?y',), 'have': ('jack',)}
#                 ],
#
#             'tighten': [['?x', '?y'], ['nut', 'hub'],
#                         {'have': [['wrench']], 'loose': [['?x', '?y']], 'on-ground': [['?y']]},
#                {'tight': ('?x', '?y')}, {'loose': ('?x', '?y')}
#                ],
#
#             'loosen':[['?x', '?y'], ['nut', 'hub'], {'have': [['wrench']], 'tight':[['?x', '?y']], 'on-ground':[['?y']]},
#                         {'loose':('?x', '?y')}, {'tight':('?x', '?y')}
#                         ],
#
#              'fetch':[['?x', '?y'], ['obj', 'container'], {'in': [['?x', '?y']], 'open':[['?y']]},
#                         {'have':('?x',)}, {'in':('?x', '?y')}
#                         ],
#              'put-away':[['?x', '?y'], ['obj', 'container'], {'have': [['?x']], 'open':[['?y']]},
#                          {'in':('?x', '?y')}, {'have':('?x',)}
#                         ]
#
# }
#
#
#
# argumentos = {
#               'tool': {'wrench', 'jack', 'pump'},
#               'obj': {'wrench', 'jack', 'pump', 'nuts1', 'r1', 'w1'},
#               'hub': {'the-hub1'},
#               'nut': {'nuts1'},
#                 'object': {'the-hub1', 'boot'},
#               'container': {'boot'},
#               'wheel': {'r1', 'w1'},
# }
#
#
#
#
# path = '../in/'
#
#
# def confere_equivalencia(dic1, dic2):
#     import collections
#     compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
#     s1 = set(dic1.keys())
#     s2 = set(dic2.keys())
#     if s1 != s2:
#         print('erro chaves')
#         print(s1)
#         print(s2)
#         exit()
#     for k in dic1:
#         print(k)
#         l1 = dic1[k]
#         l2 = dic2[k]
#         # print(l1)
#         # print(l2)
#         if not len(l1) == len(l2):
#             print('erro conteudo1')
#             print(l1)
#             print(l2)
#             # exit()
#         for i, j in zip(l1, l2):
#             if not type(i) == type(j):
#                 print('erro conteudo2')
#                 print(i)
#                 print(j)
#                 # exit()
#             if isinstance(i, list):
#                 if not compare(i, j):
#                     print('erro conteudo')
#                     print(i)
#                     print(j)
#                     # exit()
#             else:
#                 if not i.keys() == j.keys():
#                     print('erro conteudo3')
#                     print(i)
#                     print(j)
#                     # exit()
#
#
#


# print('\nHeuristica: {}'.format(nome_heuristica[heuristica]))
# estado, meta, operacoes, argumentos  = Conversor(path + problema[0], path + problema[1]).get_planner_args()
# pl = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), 'max')
#
# tempo_inicial = time.time()
# plano_estados, dicionario_expansao, contador_gerados = Busca().busca_a_estrela(pl)
# tempo_execucao = round((time.time()-tempo_inicial)*1000)
# print('O algoritmo levou {} milisegundos'.format(tempo_execucao))
#
# print('No total {} nós foram visitados\nTivemos {} e {} nós gerados\nE a taxa de ramificaçao foi de {} filhos por nó'.format(
#     len(dicionario_expansao), sum(list(dicionario_expansao.values())), contador_gerados,
#     round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2)))
#
# print('O plano possui {} passos, os quais, a partir do estado inicial, sao:'.format(len(plano_estados)))
#
# for nc, i in zip(plano_estados, range(1, len(plano_estados)+1)):
#     print('{}: '.format(i))
#     print('\t Aplicando a açao {}, gera-se o estado'.format(str(nc.operacao)))
#     print('\t\t' + str(nc.dict)+'\n')
#
#
#
# exit()

nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = [('robot_domain.pddl', 'robot_problem_2b.pddl', 'Problema do robo: 2 caixas'),
            ('robot_domain.pddl', 'robot_problem_3b.pddl', 'Problema do robo: 3 caixas'),
            ('robot_domain.pddl', 'robot_problem_4b.pddl', 'Problema do robo: 4 caixas'),
            ('robot_domain.pddl', 'robot_problem_5b.pddl', 'Problema do robo: 5 caixas'),
            ('robot_domain.pddl', 'robot_problem_6b.pddl', 'Problema do robo: 6 caixas'),
            ('robot_domain.pddl', 'robot_problem_7b.pddl', 'Problema do robo: 7 caixas'),
            ('robot_domain.pddl', 'robot_problem_8b.pddl', 'Problema do robo: 8 caixas'),
            ('robot_domain.pddl', 'robot_problem_9b.pddl', 'Problema do robo: 9 caixas'),
            ('robot_domain.pddl', 'robot_problem_10b.pddl', 'Problema do robo: 10 caixas'),
             ('tyreworld_domain.pddl', 'tyreworld_problem.pddl', 'Problema TyreWorld')]
# problemas = [('robot_domain.pddl', 'robot_problem.pddl', 'Problema do robo')]
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['um', 'soma', 'max',"FF"]

path = '../in/'
saida_estatisticas = '../estatisticas/saida_problema.txt'
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


for problema in problemas:
    print('\n\nTratando o {}'.format(problema[2]))
    for heuristica in heuristicas:
        experimento = []
        print('\nHeuristica: {}'.format(nome_heuristica[heuristica]))
        estado, meta, operacoes, argumentos  = Conversor(path + problema[0], path + problema[1]).get_planner_args()
        pl = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), heuristica)
        pl.nome_do_problema=problema[2]
        pl.gerar_grafico=True

        tempo_inicial = time.time()
        plano_estados, dicionario_expansao, contador_gerados = Busca().busca_a_estrela(pl)
        tempo_execucao = round((time.time()-tempo_inicial)*1000)

        print('O algoritmo levou {} milisegundos'.format(tempo_execucao))
        experimento.append(tempo_execucao)

        print('No total {} nós foram visitados\nTivemos {} nós gerados com repeticçoes e {} sem repetiçoes\nE a taxa de ramificaçao foi de {} filhos por nó'.format(
            len(dicionario_expansao), sum(list(dicionario_expansao.values())), contador_gerados,
            round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2)))

        experimento.append(len(dicionario_expansao))
        experimento.append(sum(list(dicionario_expansao.values())))
        experimento.append(contador_gerados)
        experimento.append(round(sum(list(dicionario_expansao.values()))/len(dicionario_expansao), 2))
        experimento.append(len(plano_estados))

        print('O plano possui {} passos, os quais, a partir do estado inicial, sao:'.format(len(plano_estados)))

        for nc, i in zip(plano_estados, range(1, len(plano_estados)+1)):
            print('{}: '.format(i))
            print('\t Aplicando a açao {}, gera-se o estado'.format(str(nc.operacao)))
            print('\t\t' + str(nc.dict)+'\n')

        estatisticas[problema[2]][heuristica] = experimento

f.write(str(estatisticas)+'\n')
f.close()