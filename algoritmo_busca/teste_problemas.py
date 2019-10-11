from algoritmo_busca.busca import Busca
from main.planejador import Estado, Planejador
from main.conversorPDDL import Conversor

#
# estado = {'box-at': {('box1', 'room1'), ('box2', 'room1'), ('box3', 'room1'), ('box4', 'room1')},
#           'robot-at': {('room1',)},
#           'free': {('right',), ('left',)}}
#
# meta = {'box-at': {('box1', 'room2'), ('box2', 'room2'), ('box3', 'room2'), ('box4', 'room2')},
#           'robot-at': {('room1',)},
#           'free': {('right',), ('left', )}}
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
# argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}


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

path = '../in/'
estado2, meta2, operacoes2, argumentos2  = Conversor(path + 'robot_domain.pddl', path + 'robot_problem.pddl').get_planner_args()
# estado2, meta2, operacoes2, argumentos2 = Conversor(path + 'tyreworld_domain.pddl', path + 'tyreworld_problem.pddl').get_planner_args()
#
# confere_equivalencia(estado, estado2)
# confere_equivalencia(meta, meta2)
# confere_equivalencia(operacoes, operacoes2)
# confere_equivalencia(argumentos, argumentos2)
# operacoes2['jack-down'][2] = {'not-on-ground': [['?y']]}
# print(operacoes2)
# exit()
p = Planejador(argumentos2, operacoes2, Estado(estado2), Estado(meta2), 'max')

import time
tempo_inicial = time.time()
no, fr = Busca().a_star_search(p)
print(fr)
print('O algoritmo levou {} milisegundos'.format(round((time.time()-tempo_inicial)*1000)))

print('\n')
for nc, i in zip(no, range(1, len(no)+1)):
    print('{}: '.format(i))
    print('\t Aplicando a açao {}, gera-se o estado'.format(str(nc.operacao)))
    print('\t\t' + str(nc.dict)+'\n')
