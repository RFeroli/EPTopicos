import math
import copy
import heapq
from graficos import GrafoGrafico
from graficos import ColorUtils

import hashlib
import base64

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
        hasher = hashlib.sha256()
        hasher.update(repr(self.make_hashable(o)).encode())
        return base64.b64encode(hasher.digest()).decode()

    def make_hashable(self, o):
        if isinstance(o, (tuple, list)):
            return tuple((self.make_hashable(e) for e in o))

        if isinstance(o, dict):
            return tuple(sorted((k, self.make_hashable(v)) for k, v in o.items()))

        if isinstance(o, (set, frozenset)):
            return tuple(sorted(self.make_hashable(e) for e in o))

        return o

    # def _gere_hash(self, o):
    #     if isinstance(o, (set, tuple, list)):
    #         return tuple([self._gere_hash(e) for e in o])
    #
    #     elif not isinstance(o, dict):
    #         return hash(o)
    #
    #     nova_estrutura = copy.deepcopy(o)
    #     for k, v in nova_estrutura.items():
    #         nova_estrutura[k] = self._gere_hash(v)
    #
    #     return hash(tuple(frozenset(sorted(nova_estrutura.items()))))
    #

    def busca_a_estrela(self, planejador):
        if(planejador.gerar_grafico):
            grafico = GrafoGrafico.GrafoGrafico()

        fila_prioridade = PriorityQueue()
        inicio = planejador.recupera_inicio()
        if (planejador.gerar_grafico):
            grafico.incluir_raiz(inicio,"raiz")#incluindo raiz
        fila_prioridade.put(inicio, 0)
        nos_expandidos = {}
        nos_ramificacao = {}
        no_pai = {}
        custo_neste_momento = {}
        hsi = self._gere_hash(inicio.dict)
        inicio.contador = hsi
        contador_gerados = 1
        no_pai[hsi] = None
        custo_neste_momento[hsi] = 0
        meta_plano = []

        while not fila_prioridade.empty():
            atual = fila_prioridade.get()

            if self._foi_expandido(nos_expandidos, atual.dict):
                continue

            nos_expandidos[atual.contador] = atual
            if planejador.equivalentes(atual.dict, planejador.recupera_meta().dict):
                hsi = self._gere_hash(atual.dict)
                while no_pai[hsi] is not None:
                    meta_plano.insert(0, nos_expandidos[hsi])
                    hsi = no_pai[hsi]
                break

            nos_ramificacao[atual.contador] = 0

            for vizinho in planejador.vizinhos(atual):
                nos_ramificacao[atual.contador] += 1
                vizinho.contador = self._gere_hash(vizinho.dict)

                novo_custo = custo_neste_momento[atual.contador] + planejador.custo_movimento(atual, vizinho)
                if vizinho.contador not in custo_neste_momento or novo_custo < custo_neste_momento[vizinho.contador]:

                    custo_neste_momento[vizinho.contador] = novo_custo
                    prioridade = planejador.heuristica(vizinho, planejador.recupera_meta())
                    contador_gerados +=1
                    if (planejador.gerar_grafico):
                        grafico.incluir_no (atual, vizinho,prioridade+novo_custo)
                    if not math.isinf(prioridade):
                        fila_prioridade.put(vizinho, (prioridade + novo_custo))
                    no_pai[vizinho.contador] = atual.contador
        if (planejador.gerar_grafico):
            grafico.tela.mudarCorArvore (ColorUtils.toHex (0, 255, 0))
            for no in meta_plano:
                grafico.tela.tradutorNo[no].mudarCorTexto (ColorUtils.toHex (0, 200, 30))
            grafico.tela.reordenarArvore()
            #grafico.tela.canvas.postscript (file="../graficos_ramificacao/grafico_" + planejador.heu + "_" + planejador.nome_do_problema.replace(" ","_")+".ps",
                                            #colormode='color')

            #grafico.tela.raiz.deiconify()


        # Esses dicionarios sao usados para extrair a solucao
        # return came_from, custo_neste_momento, nos_expandidos
        return meta_plano, nos_ramificacao, contador_gerados



