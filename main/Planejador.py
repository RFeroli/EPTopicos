from itertools import product, chain
from copy import copy, deepcopy

class Planejador:
    def __init__(self, argumentos, operacoes):
        # ambos dicionarios
        self.operacoes = operacoes
        self.argumentos = argumentos

    def devolve_possiveis_combinacoes(self, estado_atual):

        saida = {}

        for operacao in self.operacoes:
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
                print('operacao indisponivel')
                continue
            # encontre os indices das repeticoes
            unique_entries = set(l)
            indices = {value: [i for i, v in enumerate(l) if v == value] for value in unique_entries}
            # print(indices)

            # guarda os estados que respeitam as restricoes
            possiveis_estados = []
            for p in product(*lista):
                est = list(chain(*p))
                possiveis_estados.append(est)
                for variavel in indices:
                    lista_igualdades = [est[x] for x in indices[variavel]]
                    # quando cria a lista de elementos que deveriam ser iguais, caso algum seja diferente apenas retira
                    # este da lista e para de coferir
                    if not lista_igualdades[1:] == lista_igualdades[:-1]:
                        possiveis_estados.pop()
                        break

            possiveis_estados_ordenados = []
            utilizados = set()
            faltam = []
            faltam_variveis = []
            for possivel in possiveis_estados:
                est = []
                for variavel, tipo in zip(op[0], op[1]):
                    try:
                        i = l.index(variavel)
                        est.append(possivel[i])
                        utilizados.add(possivel[i])
                    except ValueError:
                        est.append(variavel)
                        faltam.append(tipo)
                        faltam_variveis.append(variavel)
                # print(est)
                possiveis_estados_ordenados.append(est)

            for item in product(possiveis_estados_ordenados,
                                *[list(self.argumentos[f].difference(utilizados)) for f in faltam]):
                s = copy(item[0])
                contador_indice = 1
                for i in range(len(s)):
                    if s[i] in faltam_variveis:
                        s[i] = item[contador_indice]
                        contador_indice += 1
                #
                saida[operacao].append(s)
        return saida

    def crie_proximo_estado(self, estado_atual, ope):
        # estado atual é um dicionario
        # operacao é uma tupla com o nome e os parametros
        nome, parametros = ope
        proximo_estado = deepcopy(estado_atual)
        operacao = self.operacoes[nome]
        d = {}
        for i, j in zip(operacao[0], parametros):
            d[i] = j

        # print(d)
        for pe in operacao[3]:
            if pe not in proximo_estado:
                proximo_estado[pe] = []
            proximo_estado[pe].append(tuple([d[x] for x in operacao[3][pe]]))

        for pe in operacao[4]:
            proximo_estado[pe].remove(tuple([d[x] for x in operacao[4][pe]]))

        return proximo_estado

estado = {'box-at': [('box4', 'room2'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')],
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


argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}



p = Planejador(argumentos, operacoes)
possiveis = p.devolve_possiveis_combinacoes(estado)

for i in possiveis:
    if possiveis[i]:
        print('{} {}'.format(i, possiveis[i][0]))
        p.crie_proximo_estado(estado, (i, possiveis[i][0]))