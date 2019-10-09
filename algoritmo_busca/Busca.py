import math
import copy

from main.planejador import Planejador, Estado

# class SimpleGraph:
#     def __init__(self):
#         self.edges = {}
#
#     def vizinhos(self, id):
#         return self.edges[id]
#
#     def is_meta(self, estado, meta):
#         return estado == meta
#
#     def custo_movimento(self, estado, proximo):
#         print("Custo de {} para {} = {}".format(estado, proximo, (ord(estado)*ord(proximo))%10 + 2))
#         return (ord(estado)*ord(proximo))%10 +2


import heapq
# from queue import PriorityQueue

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        try:
            heapq.heappush(self.elements, (priority, item))
        except:
            pass
    def get(self):
        return heapq.heappop(self.elements)[1]

# p = PriorityQueue()
# p.put('a', 10)
# p.put('ar2',5)
#
# p.put('10', 1)
#
# while not p.empty():
#     print(p.get())
# exit()

def heuristica_retorna_1(a, b):
    return 1

# TODO fazer esse metodos
def foi_expandido(expandidos, estado):
    if make_hash(estado) in expandidos:
        return True
    return False

# TODO arrumar o A*
# TODO testar as 3 heuristicas que ja foram implementadas

def make_hash(o):

  """
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """

  if isinstance(o, (set, tuple, list)):

    return tuple([make_hash(e) for e in o])

  elif not isinstance(o, dict):

    return hash(o)

  new_o = copy.deepcopy(o)
  for k, v in new_o.items():
    new_o[k] = make_hash(v)

  return hash(tuple(frozenset(sorted(new_o.items()))))


def a_star_search(planejador):
    frontier = PriorityQueue()
    inicio = planejador.recupera_inicio()
    frontier.put(inicio, 0)

    # frontier.put(inicio, 0)
    nos_expandidos = {}
    came_from = {}
    cost_so_far = {}
    hsi = make_hash(inicio.dict)
    print('Empilha {} com prioridade {}'.format(hsi, 0))
    print('Com operacao {}\n\t\t{}\n'.format(inicio.operacao, inicio.dict))
    inicio.contador = hsi
    came_from[hsi] = None
    cost_so_far[hsi] = 0

    while not frontier.empty():
        current = frontier.get()
        print('Desenpilha {}'.format(current.contador))
        print('Com operacao {}\n\t\t{}\n'.format(current.operacao, current.dict))
        if foi_expandido(nos_expandidos, current.dict):
            continue
        nos_expandidos[current.contador] = current
        if planejador.equivalentes(current.dict, planejador.recupera_meta().dict):
            break

        for next in planejador.vizinhos(current):
            next.contador = make_hash(next.dict)

            new_cost = cost_so_far[current.contador] + planejador.custo_movimento(current, next)
            if next.contador not in cost_so_far or new_cost < cost_so_far[next.contador]:
                cost_so_far[next.contador] = new_cost
                priority = planejador.heuristica(next, planejador.recupera_meta())
                if not math.isinf(priority):
                    print('Empilha {} com prioridade {}'.format(next.contador, priority + new_cost))
                    print('Com operacao {}\n\t\t{}\n'.format(next.operacao, next.dict))
                    frontier.put(next, (priority + new_cost))
                else:
                    print('Descarta'.format(next.contador, priority + new_cost))
                    print('Com operacao {}\n\t\t{}\n'.format(next.operacao, next.dict))
                came_from[next.contador] = current.contador
    print('dia')
    return came_from, cost_so_far, nos_expandidos


estado = {'box-at': {('box4', 'room2'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')},
          'robot-at': {('room1',)},
          'free': {('right',), ('left',)}}

meta = {'box-at': {('box4', 'room2'), ('box3', 'room2'), ('box1', 'room2'), ('box2', 'room2')},
          'robot-at': {('room1',)},
          'free': {('right',), ('left',)}}

# meta2 = {'box-at': [('box4', 'room2'), ('box3', 'room2'), ('box1', 'room2'), ('box2', 'room2')],
#           'robot-at': [('room1',)],
#           'free': [('left',)]}


# l = {1:estado, 2:meta}
# print(foi_expandido(l, meta2))
# exit()

# variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
operacoes = {
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
                       {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']},
                       {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']},
                        {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
                        ],
            'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}


argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}



p = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), 'max')
# for e in p.vizinhos(Estado(estado)):
#     print(e.dict)
#     pass
c, s, no = a_star_search(p)
print(c)
print(no)
# for nc in c:
#     print(nc)
#     if nc:
#         print(c[nc])
#         # print('\t'+str(c[nc].contador))
#         print('\t' + str(c[nc].operacao))
#         print('\t' + str(c[nc].dict))
#     print('\n')
print(s)


#
# example_graph = SimpleGraph()
# example_graph.edges = {
#     'A': ['B'],
#     'B': ['A', 'C', 'D'],
#     'C': ['A'],
#     'D': ['E', 'A'],
#     'E': ['B']
# }
#
# a, b = a_star_search(example_graph, "A", "E", heuristica_retorna_1)
# print(a)
# print(b)
