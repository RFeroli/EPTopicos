from itertools import product, chain
from copy import copy, deepcopy
from math import inf


class Estado:
    def __init__(self, dict):
        self.dict = dict
        self.contador = -1
        self.operacao = ''


class Planejador:
    def __init__(self, argumentos, operacoes, inicio, meta, heuristica):
        # ambos dicionarios
        self.operacoes = operacoes
        self.argumentos = argumentos
        self.estado_inicial = inicio
        self.estado_meta = meta
        self.heu = heuristica

    def recupera_inicio(self):
        return self.estado_inicial

    def recupera_meta(self):
        return self.estado_meta

    def vizinhos(self, estado_atual):
        possiveis = self.devolve_possiveis_combinacoes(estado_atual.dict)
        print(possiveis)
        vizinhos = []
        for ope in possiveis:
            for parametros in possiveis[ope]:
                vizinhos.append(self.crie_proximo_estado(estado_atual.dict, (ope, parametros)))

        return vizinhos

    def custo_movimento(self, atual, final):
        return 1

    def heuristica(self, atual, final):
        if self.heu == 'soma':
            return self.heuristica_graphplan_soma_niveis(atual, final)
        elif self.heu == 'max':
            return self.heuristica_graphplan_nivel_maximo(atual, final)
        elif self.heu == 'FF':
            return self.heuristica_fast_foward(atual, final)



    def devolve_possiveis_combinacoes(self, estado_atual):


        saida = {}

        for operacao in self.operacoes:
            # print(operacao)
            saida[operacao] = []
            op = self.operacoes[operacao]
            preconds = op[2]
            lista = []
            # print(operacao)
            try:
                l = []
                for precond in preconds:
                    l += preconds[precond]
                    lista.append(estado_atual[precond])
            except:
                # print('operacao indisponivel')
                continue
            # encontre os indices das repeticoes

            # print(l)
            # print(lista)
            unique_entries = set(l)
            indices = {value: [i for i, v in enumerate(l) if v == value] for value in unique_entries}
            # print(indices)

            # guarda os estados que respeitam as restricoes
            possiveis_estados = []
            for p in product(*lista):
                est = list(chain(*p))
                # print(est)
                possiveis_estados.append(est)
                for variavel in indices:
                    lista_igualdades = [est[x] for x in indices[variavel]]
                    # quando cria a lista de elementos que deveriam ser iguais, caso algum seja diferente apenas retira
                    # este da lista e para de coferir
                    if not lista_igualdades[1:] == lista_igualdades[:-1]:
                        possiveis_estados.pop()
                        break
            # print('-------')
            # print(possiveis_estados)
            possiveis_estados_ordenados = []
            # utilizados1 = {}
            utilizados = set()
            faltam = set()
            faltam_variveis = []
            for possivel, pos in zip(possiveis_estados, range(len(possiveis_estados))):
                est = []
                # utilizados1[pos] = set()
                for variavel, tipo in zip(op[0], op[1]):
                    try:
                        i = l.index(variavel)
                        est.append(possivel[i])
                        # utilizados1[pos].add(possivel[i])
                        utilizados.add(possivel[i])
                    except ValueError:
                        est.append(variavel)
                        faltam.add(tipo)
                        faltam_variveis.append(variavel)
                # print(est)
                possiveis_estados_ordenados.append(est)
            # print(possiveis_estados_ordenados)
            # print(utilizados)
            # print(utilizados1)
            for item in product(possiveis_estados_ordenados,
                                *[list(self.argumentos[f]) for f in faltam]):
                # print(item)
                s = copy(item[0])
                contador_indice = 1
                for i in range(len(s)):
                    if s[i] in faltam_variveis:
                        s[i] = item[contador_indice]
                        contador_indice += 1

                if len(s) == len(set(s)):
                    saida[operacao].append(s)
        return saida

    def _tupla_existe(self, lista, tupla):
        return tupla in lista

    def crie_proximo_estado(self, estado_atual, ope):
        # estado atual é um dicionario
        # operacao é uma tupla com o nome e os parametros
        nome, parametros = ope
        proximo_estado = deepcopy(estado_atual)
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j

        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = []
            t = tuple([d[x] for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].append(t)

        for pe in operacao[4]:
            proximo_estado[pe].remove(tuple([d[x] for x in operacao[4][pe]]))
            if not proximo_estado[pe]:
                del proximo_estado[pe]

        ne = Estado(proximo_estado)
        ne.operacao = ope
        return ne

    def crie_proximo_estado_graph_plan(self, estado_atual, ope):
        nome, parametros = ope
        proximo_estado = deepcopy(estado_atual)
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j

        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = []
            t = tuple([d[x] for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].append(t)

        return proximo_estado

    def equivalentes(self, atual, meta):
        for predicado in meta:
            if predicado not in atual:
                return False
            argumentos = meta[predicado]
            for arg in argumentos:
                if arg not in atual[predicado]:
                    return False

        return True



    def lista_niveis(self, estado_inicial, estado_final):
        estado = estado_inicial
        dict_niveis = []
        dict_niveis.append(estado_inicial)
        encontrou = False
        while True:
            # print('\n\nNivel {}'.format(nivel))
            possiveis = self.devolve_possiveis_combinacoes(estado)
            for i in possiveis:
                if possiveis[i]:
                    for j in possiveis[i]:
                        estado = self.crie_proximo_estado_graph_plan(estado, (i, j))

            dict_niveis.append(estado)
            if self.equivalentes(estado.dict, estado_final.dict):
                encontrou = True
                break

            if len(dict_niveis) > 1 and self.equivalentes(dict_niveis[-2].dict, dict_niveis[-1].dict):
                break

        return dict_niveis, encontrou

    def heuristica_graphplan_nivel_maximo(self, estado_atual, estado_meta):
        lista, encontrou = self.lista_niveis(estado_atual, estado_meta)
        if encontrou:
            return len(lista)-1
        return inf

    def heuristica_graphplan_soma_niveis(self, estado_atual, meta):
        lista, encontrou = self.lista_niveis(estado_atual, meta)
        if not encontrou:
            return inf
        estado_meta = deepcopy(meta)
        soma = 0
        # print(lista)
        for i in range(len(lista)):

            for pred in estado_meta:
                if pred in lista[i]:
                    comprimento = len(estado_meta[pred])
                    estado_meta[pred] = [x for x in  estado_meta[pred] if x not in lista[i][pred]]
                    soma += (i)*(comprimento-len(estado_meta[pred]))

        # print(soma)
        return soma


    # Fast Foward
    def lista_niveis_fast_forward(self, estado_inicial, estado_final):
        estado = estado_inicial
        dict_niveis = []
        dict_niveis.append(estado_inicial)
        encontrou = False
        while True:
            # print('\n\nNivel {}'.format(nivel))
            possiveis = p.devolve_possiveis_combinacoes(estado)
            for i in possiveis:
                if possiveis[i]:
                    for j in possiveis[i]:
                        estado = p.crie_proximo_estado_graph_plan(estado, (i, j))

            dict_niveis.append(estado)
            if self.equivalentes(estado, estado_final):
                encontrou = True
                break

            if len(dict_niveis) > 1 and self.equivalentes(dict_niveis[-2], dict_niveis[-1]):
                break

        return dict_niveis, encontrou


    def heuristica_fast_foward(self, estado_atual, meta):
        lista, encontrou = self.lista_niveis_fast_forward(estado_atual, meta)


# estado = {'box-at': [('box4', 'room2'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')],
#           'robot-at': [('room1',)],
#           'free': [('right',), ('left',)]}
#
# meta = {'box-at': [('box4', 'room2'), ('box3', 'room2'), ('box1', 'room2'), ('box2', 'room2')],
#           'robot-at': [('room1',)],
#           'free': [('right',), ('left',)]}
#
# # variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
# operacoes = {
#              'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
#                        {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']},
#                        {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],
#
#              'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']},
#                         {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
#                         ],
#             'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}
#
#
# argumentos = {'room': {'room1', 'room2', 'room3'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}
#
#
#
# p = Planejador(argumentos, operacoes, estado, meta, 'max')
# print(p.vizinhos(estado))
#
# p.heuristica_graphplan_soma_niveis(estado, meta)
# for i in p.lista_niveis(estado, meta):
#     print(i)

# print(p._equivalentes(estado, meta))


# print(estado)
# for nivel in range(3):
#     print('\n\nNivel {}'.format(nivel))
#     possiveis = p.devolve_possiveis_combinacoes(estado)
#     for i in possiveis:
#         if possiveis[i]:
#             for j in possiveis[i]:
#                 print('{} {}'.format(i, j))
#                 estado = p.crie_proximo_estado_graph_plan(estado, (i, j))
#                 print(estado)
#                 print('\n')
#
