import hashlib
import base64

def _gere_hash(o):
    hasher = hashlib.sha256()
    hasher.update(repr(make_hashable(o)).encode())
    return base64.b64encode(hasher.digest()).decode()


def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o


estado = {'robot-at': {('room1',)}, 'box-at': {('box2', 'room1'), ('box3', 'room1'), ('box1', 'room1')}, 'free': {('right',), ('left',)}}
meta = {'box-at': {('box1', 'room2'), ('box2', 'room2'), ('box3', 'room2')}}
operacoes = {'move': [['?x', '?y'], ['room', 'room'], {'robot-at': [['?x']]}, {'robot-at': ('?y',)}, {'robot-at': ('?x',)}], 'pickup': [['?x', '?y', '?w'], ['box', 'arm', 'room'], {'free': [['?y']], 'robot-at': [['?w']], 'box-at': [['?x', '?w']]}, {'carry': ('?x', '?y')}, {'box-at': ('?x', '?w'), 'free': ('?y',)}], 'putdown': [['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': [['?x', '?y']], 'robot-at': [['?w']]}, {'box-at': ('?x', '?w'), 'free': ('?y',)}, {'carry': ('?x', '?y')}]}
argumentos = {'room': {'room1', 'room2'}, 'box': {'box2', 'box3', 'box1'}, 'arm': {'left', 'right'}}



# estado = {'robot-at':{('room1',)},
# 'box-at':{('box3', 'room1'), ('box1', 'room1'), ('box2', 'room1')},
# 'free':{('left',), ('right',)}}

#  #('robot-at', ('room1',)) -> [n, [#op0, #op0, ..., #opn-1]]
atributos_anteriores = {
    _gere_hash(('robot-at', ['room1'])) : [-1, set()],
    _gere_hash(('box-at', ['box1', 'room1'])) : [-1, set()],
    _gere_hash(('box-at', ['box2', 'room1'])) : [-1, set()],
    _gere_hash(('box-at', ['box3', 'room1'])) : [-1, set()],
    _gere_hash(('free', ['right'])) : [-1, set()],
    _gere_hash(('free', ['left'])) : [-1, set()],
}

#  #opN -> [precond1, precond2, ...., precondN]
operacoes_preconds = {}


# ope = (nome, parametros)
def insere_operacao(ope):
    nome, parametros = ope
    precondicoes = operacoes[nome][2]
    variaveis = operacoes[nome][0]
    d = {}
    for i, j in zip(variaveis, parametros):
        d[i] = j
    hash_atual = _gere_hash(ope)
    # print('hash de {} : {}'.format(ope, hash_atual))
    operacoes_preconds[hash_atual] = []
    for precond in precondicoes:
        for el in precondicoes[precond]:
            arg = [d[x] for x in el]
            operacoes_preconds[hash_atual].append((precond, arg))
            # print(el)

def devolve_custo_operacao(hash_ope):
    l = operacoes_preconds[hash_ope]
    return sum([max(0, atributos_anteriores[_gere_hash(x)][0]) for x in l])

def devolve_operacoes(hash_ope):
    l = operacoes_preconds[hash_ope]
    conjunto_saida = set()
    for x in l:
        conjunto_saida = conjunto_saida.union(atributos_anteriores[_gere_hash(x)][1])

    return conjunto_saida

def insere_atributos(predicado, ope):
    hash_ope = _gere_hash(ope)
    hash_precidado = _gere_hash(predicado)
    if hash_precidado not in atributos_anteriores:
        conjunto = devolve_operacoes(hash_ope)
        conjunto.add(hash_ope)
        atributos_anteriores[_gere_hash(hash_precidado)] = [len(conjunto), conjunto]
    else:
        custo_atual = devolve_custo_operacao(hash_ope)
        if atributos_anteriores[hash_precidado][0] > custo_atual+1:
            conjunto = devolve_operacoes(hash_ope)
            conjunto.add(hash_ope)
            atributos_anteriores[hash_precidado] = [len(conjunto), conjunto]



insere_operacao(('move', ('room1', 'room2')))
insere_operacao(('pickup', ('box1', 'right', 'room1')))
insere_operacao(('pickup', ('box1', 'left', 'room1')))
insere_operacao(('pickup', ('box2', 'right', 'room1')))
insere_operacao(('pickup', ('box2', 'left', 'room1')))
insere_operacao(('pickup', ('box3', 'right', 'room1')))
insere_operacao(('pickup', ('box3', 'left', 'room1')))


insere_atributos(('robot-at', ['room2']), ('move', ('room1', 'room2')))
insere_atributos(('carry', ['box1', 'right']), ('pickup', ('box1', 'right', 'room1')))
insere_atributos(('carry', ['box1', 'left']), ('pickup', ('box1', 'left', 'room1')))
insere_atributos(('carry', ['box2', 'right']), ('pickup', ('box2', 'right', 'room1')))
insere_atributos(('carry', ['box2', 'left']), ('pickup', ('box2', 'left', 'room1')))
insere_atributos(('carry', ['box3', 'right']), ('pickup', ('box3', 'right', 'room1')))
insere_atributos(('carry', ['box3', 'left']), ('pickup', ('box3', 'left', 'room1')))



#
print()
# print(devolve_custo_operacao(_gere_hash(('pickup', ('box1', 'right', 'room1')))))
# print(operacoes_preconds)