from copy import deepcopy
def _gere_hash(o):
    if isinstance (o, (set, tuple, list)):
        return tuple ([_gere_hash (e) for e in o])

    elif not isinstance (o, dict):
        return hash (o)

    nova_estrutura = deepcopy (o)
    for k, v in nova_estrutura.items ():
        nova_estrutura[k] = _gere_hash (v)

    return hash (tuple (frozenset (sorted (nova_estrutura.items ()))))

g = {'robot-at':{('room1',)}, 'box-at': {('box1', 'room1'), ('box2', 'room1')}, 'free' :{('left',), ('right',)}}

f = {'robot-at':{('room1',)}, 'box-at': {('box4', 'room1'), ('box1', 'room1'), ('box2', 'room1'), ('box3', 'room1')}, 'free' :{('right',), ('left',)}}

print(_gere_hash(g))
print(_gere_hash(f))