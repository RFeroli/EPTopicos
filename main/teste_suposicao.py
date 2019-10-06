from itertools import product

estado = {'box-at': [('box4', 'room1'), ('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')],
          'robot-at': [('room1',)],
          'free': [('right',), ('left',)]}

operacoes = {
             'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}],
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']}]}


argumentos = {'room': ['room1', 'room2'], 'box': ['box1', 'box2', 'box3', 'box4'], 'arm': ['right', 'left']}



for operacao in operacoes:
    op = operacoes[operacao]
    #
    # variaveis = op[0]
    # tipos = [1]
    #
    # dicionario = {}
    # for v, t in zip(variaveis, tipos):
    #     dicionario[v] = argumentos[t]

    preconds = op[2]
    lista = []
    try:
        l = []
        for precond in preconds:
            l +=preconds[precond]
            lista.append(estado[precond])

    # print(lista)
        print(l)
        for p in product(*lista):
            print(p)
    except:
        print('operacao impossivel')
    # exit()


