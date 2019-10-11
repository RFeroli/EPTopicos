import math
import copy

from main.planejador import Planejador, Estado

import heapq

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

class Busca:

    def _foi_expandido(self, expandidos, estado):
        if self._gere_hash(estado) in expandidos:
            return True
        return False

    def _gere_hash(self, o):
      if isinstance(o, (set, tuple, list)):
        return tuple([self._gere_hash(e) for e in o])

      elif not isinstance(o, dict):
        return hash(o)

      new_o = copy.deepcopy(o)
      for k, v in new_o.items():
        new_o[k] = self._gere_hash(v)

      return hash(tuple(frozenset(sorted(new_o.items()))))


    def a_star_search(self, planejador):
        frontier = PriorityQueue()
        inicio = planejador.recupera_inicio()
        frontier.put(inicio, 0)
        nos_expandidos = {}
        nos_ramificacao = {}
        came_from = {}
        cost_so_far = {}
        hsi = self._gere_hash(inicio.dict)
        # print('Empilha {} com prioridade {}'.format(hsi, 0))
        # print('Com operacao {}\n\t\t{}\n'.format(inicio.operacao, inicio.dict))
        inicio.contador = hsi
        came_from[hsi] = None
        cost_so_far[hsi] = 0
        meta_path = []

        while not frontier.empty():
            current = frontier.get()
            # print('Desenpilha {}'.format(current.contador))
            # print('Com operacao {}\n\t\t{}\n'.format(current.operacao, current.dict))
            if self._foi_expandido(nos_expandidos, current.dict):
                continue

            nos_expandidos[current.contador] = current
            if planejador.equivalentes(current.dict, planejador.recupera_meta().dict):
                hsi = self._gere_hash(current.dict)
                while came_from[hsi] is not None:
                    meta_path.insert(0, nos_expandidos[hsi])
                    hsi = came_from[hsi]
                break

            nos_ramificacao[current.contador] = 0

            for vizinho in planejador.vizinhos(current):

                nos_ramificacao[current.contador] +=1
                vizinho.contador = self._gere_hash(vizinho.dict)

                new_cost = cost_so_far[current.contador] + planejador.custo_movimento(current, vizinho)
                if vizinho.contador not in cost_so_far or new_cost < cost_so_far[vizinho.contador]:
                    cost_so_far[vizinho.contador] = new_cost
                    priority = planejador.heuristica(vizinho, planejador.recupera_meta())
                    if not math.isinf(priority):
                        # print('Empilha {} com prioridade {}'.format(next.contador, priority + new_cost))
                        # print('Com operacao {}\n\t\t{}\n'.format(next.operacao, next.dict))
                        frontier.put(vizinho, (priority + new_cost))
                    # else:
                    #     print('Descarta'.format(next.contador, priority + new_cost))
                    #     print('Com operacao {}\n\t\t{}\n'.format(next.operacao, next.dict))
                    came_from[vizinho.contador] = current.contador

        # Esses dicionarios sao usados para extrair a solucao
        # return came_from, cost_so_far, nos_expandidos

        return meta_path, nos_ramificacao
