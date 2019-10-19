from itertools import product, chain
from copy import copy, deepcopy
from math import inf
from main import grafoFF
import hashlib
import base64

class Estado:
    def __init__(self, dict):
        self.dict = dict
        self.contador = -1
        self.operacao = ''

    def __lt__(self, other):
        return False


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
    #
    # def _gere_hash(self, o):
    #   if isinstance(o, (set, tuple, list)):
    #     return tuple([self._gere_hash(e) for e in o])
    #
    #   elif not isinstance(o, dict):
    #     return hash(o)
    #
    #   nova_estrutura = deepcopy(o)
    #   for k, v in nova_estrutura.items():
    #     nova_estrutura[k] = self._gere_hash(v)
    #
    #   return hash(tuple(frozenset(sorted(nova_estrutura.items()))))

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

    def vizinhos(self, estado_atual):
        possiveis = self.devolve_possiveis_combinacoes(estado_atual.dict)
        # print(possiveis)
        vizinhos = []

        for ope in possiveis:
            for parametros in possiveis[ope]:
                vizinhos.append(self.crie_proximo_estado(estado_atual.dict, (ope, parametros)))

        return vizinhos

    def custo_movimento(self, atual, final):
        return 1

    def heuristica(self, atual, final):
        if self.heu == 'soma':
            return self.heuristica_graphplan_soma_niveis(atual.dict, final.dict)
        elif self.heu == 'max':
            return self.heuristica_graphplan_nivel_maximo(atual.dict, final.dict)
        elif self.heu == 'FF':
            return self.heuristica_ff(atual.dict, final.dict)
        elif self.heu == 'um':
            return self.heuristica_um(atual.dict, final.dict)

    def _deste_tipo(self, nome_obj, tipo):
        return nome_obj in self.argumentos[tipo]


    def _confere_precondicoes(self, estado_atual, preconds, op):
        lista = []
        l = []

        for precond in preconds:
            if precond not in estado_atual:
                return [], []
            for p in preconds[precond]:
                if all([True if "?" not in x else False for x in p]):
                    for el in p:
                        if (el,) not in estado_atual[precond]:
                            return [], []
                else:
                    # auxl = [x for x in p if "?" in x]
                    l += p
                    nova_lista_aux = []
                    if precond not in estado_atual:
                        return [], []

                    for et in estado_atual[precond]:
                        for i, j in zip(p, et):
                            indice = op[0].index(i)
                            tipo = op[1][indice]
                            if not self._deste_tipo(j, tipo):
                                break
                        else:
                            nova_lista_aux.append(et)
                    lista.append(nova_lista_aux)
        elem = [x for x in lista if x]
        if not elem:
            print(elem)

        return lista, l

    def devolve_possiveis_combinacoes(self, estado_atual):
        saida = {}

        for operacao in self.operacoes:
            # print(operacao)
            op = self.operacoes[operacao]
            preconds = op[2]
            # lista = []
            lista, l = self._confere_precondicoes(estado_atual, preconds, op)
            if not lista or not l:
                continue

            saida[operacao] = []

            unique_entries = set(l)
            indices = {value: [i for i, v in enumerate(l) if v == value] for value in unique_entries}
            indices_conferir = [[i for i, v in enumerate(l) if v == value] for value in unique_entries if len([i for i, v in enumerate(l) if v == value]) > 1]
            # print(indices)

            # guarda os estados que respeitam as restricoes
            possiveis_estados_ordenados = []
            posicao = 0
            utilizados = {}
            for p in product(*lista):
                est = list(chain(*p))
                # print(est)

                # possiveis_estados.append(est)
                for confere in indices_conferir:
                    lista_igualdades = [est[x] for x in confere]
                    # quando cria a lista de elementos que deveriam ser iguais, caso algum seja diferente apenas retira
                    # este da lista e para de coferir
                    if not lista_igualdades[1:] == lista_igualdades[:-1]:
                        # possiveis_estados.pop()
                        break

                else:
                    possivel = [est[indices[x][0]] if x in indices else x for x in op[0]]
                    utilizados[posicao] = set(possivel)
                    posicao+=1
                    possiveis_estados_ordenados.append(possivel)

            # print('-------')
            if possiveis_estados_ordenados:
                faltam = [(possiveis_estados_ordenados[0][x], op[1][x]) for x in range(len(possiveis_estados_ordenados[0])) if '?' in possiveis_estados_ordenados[0][x]]

            if not faltam:
                saida[operacao] = possiveis_estados_ordenados
                continue
            # print(faltam)

            for item in range(len(possiveis_estados_ordenados)):
                complementos = []
                for f in faltam:
                    complementos.append([d for d in self.argumentos[f[1]] if d not in utilizados[item]])
                    # print(f)
                    # print(utilizados[item])
                for linha in product([possiveis_estados_ordenados[item]], *complementos):
                    # print(linha)
                    s = copy(linha[0])
                    contador = 1
                    for el in range(len(s)):
                        if '?' in s[el]:
                            s[el] = linha[contador]
                            contador+=1
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
                proximo_estado[pe] = set()
            t = tuple([d[x] if x in d else x for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].add(t)

        for pe in operacao[4]:
            # print(1)

            proximo_estado[pe].remove(tuple([d[x] if x in d else x for x in operacao[4][pe]]))
            if not proximo_estado[pe]:
                del proximo_estado[pe]

        ne = Estado(proximo_estado)
        ne.operacao = ope
        return ne

    def calcula_efeitos_e_precondicoes(self, estado_atual, ope):
        nome, parametros = ope
        efeitos = {}
        operacao = self.operacoes[nome]
        preconds={}
        preconds={}
        d = {}
        for i, j in zip (operacao[0], parametros):
            d[i] = j

        for precond in operacao[2]:
            preconds[precond]=set()
            for arg1 in operacao[2][precond]:
                preconds[precond].add(tuple([d[x] if x in d else x for x in arg1]))

        for pe in operacao[3]:
            if pe not in efeitos:
                efeitos[pe] = set ()
            t = tuple ([d[x] if x in d else x for x in operacao[3][pe]])
            if not self._tupla_existe (efeitos[pe], t):
                efeitos[pe].add (t)
        return efeitos,preconds

    def crie_proximo_estado_graph_plan(self, estado_atual, ope):
        nome, parametros = ope
        proximo_estado = deepcopy(estado_atual)
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j

        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = set()
            t = tuple([d[x] if x in d else x for x in operacao[3][pe]])
            # t = tuple([d[x] for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].add(t)

        return proximo_estado


    def crie_proximo_estado_graph_plan_alterando(self, estado_atual, ope):
        nome, parametros = ope
        proximo_estado = estado_atual
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j

        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = set()
            t = tuple([d[x] if x in d else x for x in operacao[3][pe]])
            # t = tuple([d[x] for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].add(t)

        return proximo_estado

    def equivalentes(self, atual, meta):
        for predicado in meta:
            if len(meta[predicado] - atual.get(predicado, set())):
                return False
        return True

    def heuristica_ff(self, estado_inicial, estado_final):
        estado = estado_inicial
        dict_niveis = []
        dict_niveis.append(estado_inicial)
        encontrou = False

        gff=grafoFF.GrafoFF()
        nivel=1
        while True:
            # print('\n\nNivel {}'.format(nivel))
            gff.incluir_noOps (estado, nivel)
            possiveis = self.devolve_possiveis_combinacoes(estado)
            for i in possiveis:
                if possiveis[i]:
                    for j in possiveis[i]:
                        efeitos, preconds = self.calcula_efeitos_e_precondicoes (estado, (i, j))
                        gff.incluir(preconds,(i,j),efeitos,nivel)
                        estado = self.crie_proximo_estado_graph_plan (estado, (i, j))

            dict_niveis.append(estado)
            #print(len(gff.nos))
            nivel += 1
            if self.equivalentes(estado, estado_final):
                encontrou = True
                break

            if len(dict_niveis) > 1 and self.equivalentes(dict_niveis[-2], dict_niveis[-1]):
                break

            # parte do calculo
           # print("nivel-->",nivel)
        valor_heuristica=0
        for predicado in estado_final:
             for args in estado_final[predicado]:
                no = gff.No ((predicado, {args}), nivel)
                if (not no["hash"] in gff.nos):
                    gff.nos[no["hash"]] = no
                no = gff.nos[no["hash"]]
                valor_heuristica+=self.f(no)



        #print(valor_heuristica)
        return valor_heuristica


    def f(self,no):
        soma=0
        if(no["operacao"]):
            if(no["valor"][0]!="NO-OP"and not no["flag"]):
                soma+=1
                no["flag"]=True
            for anterior in no["anteriores"]:
                #print(anterior["valor"])
                #print ("valor",self.f (anterior))
                soma+=self.f(anterior)
            return soma
        else:
            conj=[x for x in no["anteriores"] if x["valor"][0]=="NO-OP"]
            for anterior in conj:
                #print(self.f(anterior))
                return soma+self.f(anterior)
            for anterior in no["anteriores"]:
                #print (self.f (anterior))
                return soma+self.f (anterior)
        return soma

    def busca_meta(self, atual, meta):
        contador = 0
        terminou = False
        maximo = 0
        for predicado in meta:
            l = len(meta[predicado])
            meta[predicado] = meta[predicado] - atual.get(predicado, set())
            l2 = len(meta[predicado])
            contador += l - l2
            maximo = max(l2, maximo)
        if not maximo:
            terminou = True
        return contador, terminou



    def lista_niveis(self, estado_inicial, estado_final):

        estado = deepcopy(estado_inicial)
        meta = deepcopy(estado_final)
        custo_somadando_niveis = 0
        niveis = 0
        encontrou = False
        while True:
            retirado_nivel, terminou = self.busca_meta(estado, meta)
            custo_somadando_niveis+=(niveis*retirado_nivel)
            if terminou:
                encontrou = True
                break
            # print('\n\nNivel {}'.format(nivel))
            niveis+=1
            possiveis = self.devolve_possiveis_combinacoes(estado)
            hash_anterior = self._gere_hash(estado)
            for i in possiveis:
                for j in possiveis[i]:
                    estado = self.crie_proximo_estado_graph_plan_alterando(estado, (i, j))

            if hash_anterior == self._gere_hash(estado):
                break

        return niveis, custo_somadando_niveis, encontrou

    def heuristica_graphplan_nivel_maximo(self, estado_atual, estado_meta):
        niveis, custo_somadando_niveis, encontrou = self.lista_niveis(estado_atual, estado_meta)
        if encontrou:
            return niveis
        return inf

    def heuristica_um(self, estado_atual, meta):
        return 1

    def heuristica_graphplan_soma_niveis(self, estado_atual, meta):
        niveis, custo_somadando_niveis, encontrou = self.lista_niveis(estado_atual, meta)
        if not encontrou:
            return inf

        return custo_somadando_niveis

    # Fast Foward wesley
    def crie_proximo_estado_graph_plan_ff(self, estado_atual, ope, niveis_operacao_geradora, nivel):
        nome, parametros = ope
        proximo_estado = estado_atual
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j
        # niveis_operacao_geradora[nivel][self._gere_hash(ope)] =
        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = set()
            t = tuple([d[x] if x in d else x for x in operacao[3][pe]])
            # t = tuple([d[x] for x in operacao[3][pe]])
            if not self._tupla_existe(proximo_estado[pe], t):
                proximo_estado[pe].add(t)

        return proximo_estado


    def lista_niveis_fast_forward(self, estado_inicial, estado_final):
        estado = deepcopy(estado_inicial)
        encontrou = False
        ant_pred, ant_op = {}, {}
        nivel = 0
        ant_pred[nivel] = {}
        for predicado in estado:
            for t in estado[predicado]:
                ant_pred[nivel][self._gere_hash((predicado, t))] = [None]

        while True:
            # print('\n\nNivel {}'.format(nivel))
            if self.equivalentes(estado, estado_final):
                encontrou = True
                break
            # niveis_operacao_geradora[nivel] = {}
            # for predicado in estado:
            #     for t in estado[predicado]:
            #         niveis_operacao_geradora[nivel][self._gere_hash([predicado, t])]

            # possiveis = self.devolve_possiveis_combinacoes(estado)
            # niveis_operacao_geradora[nivel] = {}
            # for i in possiveis:
            #     if possiveis[i]:
            #         for j in possiveis[i]:
            #             estado = self.crie_proximo_estado_graph_plan_ff(estado, (i, j), niveis_operacao_geradora, nivel)
            #
            #
            # if len(dict_niveis) > 1 and self.equivalentes(dict_niveis[-2], dict_niveis[-1]):
            #     break
            #



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
