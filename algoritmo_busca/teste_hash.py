import hashlib
import base64
import time
from pprint import pformat
import collections
import maps

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



def dict_hash(the_dict, *ignore):
    if ignore:  # Sometimes you don't care about some items
        interesting = the_dict.copy()
        for item in ignore:
            if item in interesting:
                interesting.pop(item)
        the_dict = interesting
    result = hashlib.sha1(
        '%s' % sorted(the_dict.items())
    ).hexdigest()
    return result

operacoes = {
             'pickup':[['?x', '?y', '?w'], ['box', 'arm', 'room'],
                       {'free': ['?y'], 'robot-at':['?w'], 'box-at': ['?x', '?w']},
                       {'carry':('?x', '?y')}, {'free':('?y',), 'box-at': ('?x', '?w')}],

             'putdown':[['?x', '?y', '?w'], ['box', 'arm', 'room'], {'carry': ['?x', '?y'], 'robot-at':['?w']},
                        {'free':('?y',), 'box-at': ('?x', '?w')}, {'carry':('?x', '?y')}
                        ],
            'move':[['?x', '?y'], ['room', 'room'], {'robot-at':['?x']}, {'robot-at':('?y', )}, {'robot-at':('?x', )}]}



it  = time.time()
print(hash(maps.FrozenMap(operacoes)))
print(time.time()-it)

