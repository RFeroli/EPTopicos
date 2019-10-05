# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def vizinhos(self, id):
        return self.edges[id]

    def is_meta(self, estado, meta):
        return estado == meta

    def custo_movimento(self, estado, proximo):
        print("Custo de {} para {} = {}".format(estado, proximo, (ord(estado)*ord(proximo))%10 + 2))
        return (ord(estado)*ord(proximo))%10 +2

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


def heuristica_retorna_1(a, b):
    return 1


def a_star_search(grafo, inicio, meta, heuristica):
    frontier = PriorityQueue()
    frontier.put(inicio, 0)
    came_from = {}
    cost_so_far = {}
    came_from[inicio] = None
    cost_so_far[inicio] = 0

    while not frontier.empty():
        current = frontier.get()

        if grafo.is_meta(current, meta):
            break

        for next in grafo.vizinhos(current):
            new_cost = cost_so_far[current] + grafo.custo_movimento(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristica(meta, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


example_graph = SimpleGraph()
example_graph.edges = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
}

a, b = a_star_search(example_graph, "A", "E", heuristica_retorna_1)
print(a)
print(b)