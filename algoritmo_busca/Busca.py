import math

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

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):

        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

p = PriorityQueue()
p.put(Estado({'a':5, 4:'ar2'}), 5)
p.put({'a':15, 4:'ar2'}, 15)

p.put({'a':1, 4:'ar2'}, 1)

while not p.empty():
    print(p.get())


def heuristica_retorna_1(a, b):
    return 1


def a_star_search(planejador):
    frontier = PriorityQueue()
    inicio = planejador.recupera_inicio()
    frontier.put(inicio, 0)
    nos_descobertos = {}
    counter = 0
    inicio.contador = counter
    counter+=1
    came_from = {}
    cost_so_far = {}
    came_from[inicio.contador] = None
    cost_so_far[inicio.contador] = 0

    while not frontier.empty():
        current = frontier.get()

        if planejador.equivalentes(current.dict, planejador.recupera_meta().dict):
            break

        for next in planejador.vizinhos(current):
            next.contador = counter
            counter+=1
            new_cost = cost_so_far[current.contador] + planejador.custo_movimento(current, next)
            if next.contador not in cost_so_far or new_cost < cost_so_far[next.contador]:
                cost_so_far[next.contador] = new_cost
                priority = new_cost + planejador.heuristica(next, planejador.recupera_meta())

                if not math.isinf(priority):
                    frontier.put(next, priority)
                came_from[next.contador] = current

    return came_from, cost_so_far


estado = {'box-at': [('box4', 'room2'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')],
          'robot-at': [('room1',)],
          'free': [('right',), ('left',)]}

meta = {'box-at': [('box4', 'room2'), ('box3', 'room2'), ('box1', 'room2'), ('box2', 'room2')],
          'robot-at': [('room1',)],
          'free': [('right',), ('left',)]}

# variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
operacoes = {
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
                       {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']},
                       {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']},
                        {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
                        ],
            'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}


argumentos = {'room': {'room1', 'room2', 'room3'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}



p = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), 'max')
# for e in p.vizinhos(Estado(estado)):
#     print(e.dict)
#     pass
c, s = a_star_search(p)
print(c)
for nc in c:
    print(nc)
    if nc:
        print(c[nc])
        print('\t'+str(c[nc].contador))
        print('\t' + str(c[nc].operacao))
        print('\t' + str(c[nc].dict))
    print('\n')
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
