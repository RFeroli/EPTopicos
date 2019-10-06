from itertools import product, chain
from copy import copy

estado = {'box-at': [('box4', 'room2'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')],
          'robot-at': [('room2',)],
          'free': [('right',), ('left',)]}

operacoes = {
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
                       {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']},
                       {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']},
                        {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
                        ],
            'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}


argumentos = {'room': {'room1', 'room2'}, 'box': {'box1', 'box2', 'box3', 'box4'}, 'arm': {'right', 'left'}}




def devolve_proximos_estados():
    for operacao in operacoes:
        op = operacoes[operacao]
        preconds = op[2]
        lista = []
        print(operacao)
        try:
            l = []
            for precond in preconds:
                l +=preconds[precond]
                lista.append(estado[precond])
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
        # print('possiveis ')
        # print(l)
        # print(possiveis_estados)
        # print(op[0])

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

        print(utilizados)
        print(possiveis_estados_ordenados)
        print('combinacoes')
        # print(list(product([possiveis_estados_ordenados], *[argumentos[f].difference(utilizados) for f in faltam])))
        saida = []
        # print(faltam)
        # print(*[argumentos[f].difference(utilizados) for f in faltam])
        for item in product(possiveis_estados_ordenados, *[list(argumentos[f].difference(utilizados)) for f in faltam]):
            # print(item)
            s = copy(item[0])
            # print(s)
            contador_indice = 1
            for i in range(len(s)):
                if s[i] in faltam_variveis:
                    s[i] = item[contador_indice]
                    contador_indice+=1
            #
            saida.append(s)
            # print(s)
        print(saida)
        # print('\n\n')
        # combinacoes = {}
        # for p in possiveis_estados:
        #     for variavel in indices:
        #         combinacoes[variavel] = p[indices[variavel][0]]
        # print(combinacoes)
        # except Exception as e:
        #     print(e)
        # exit()


devolve_proximos_estados()