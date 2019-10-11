from algoritmo_busca.busca import Busca
from main.planejador import Estado, Planejador



estado = {'box-at': {('box1', 'room1'), ('box2', 'room1'), ('box3', 'room1'), ('box4', 'room1')},
          'robot-at': {('room1',)},
          'free': {('right',), ('left',)}}

meta = {'box-at': {('box1', 'room2'), ('box2', 'room2'), ('box3', 'room2'), ('box4', 'room2')},
          'robot-at': {('room1',)},
          'free': {('right',), ('left', )}}


# variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
operacoes = {
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
                       {'free': [['?y']], 'robot-at':[['?w']], 'box-at': [['?x', '?w']]},
                       {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': [['?x', '?y']], 'robot-at':[['?w']]},
                        {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
                        ],
            'move':[['?x', '?y'], ['room', 'room'], {'robot-at':[['?x']]}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}


argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}

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
#              {'on': ('?x', '?y'), 'free': ('?y',)}, {'have': ('?x', )}
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
#              {'not-on-ground': [['?y']], 'unfastened': [['?y']], 'have': [['?x'], ['wrench']]},
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
#               'container': {'boot'},
#               'wheel': {'r1', 'w1'},
# }




p = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), 'soma')

import time
tempo_inicial = time.time()
no, fr = Busca().a_star_search(p)
print('O algoritmo levou {} milisegundos'.format(round((time.time()-tempo_inicial)*1000)))

print(no)
for nc in no:
    print(str(nc.contador))
    print(str(nc.operacao))
    print('\t' + str(nc.dict))
    print()
