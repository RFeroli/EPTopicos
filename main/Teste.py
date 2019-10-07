import os
from main.pddlparser import PDDLParser
from main.domain import Domain
from main.condition_checker import Checker
import re

path = '../in/'


robot_domain = PDDLParser().parse(path + 'robot_domain.pddl')
robot_problem = PDDLParser().parse(path + 'robot_problem.pddl')

arguments = {}


for k, v in robot_problem.objects.items():
    arguments[k] = set(v)

predicates = {}
for p in robot_domain.predicates:
    predicates[p.name] = [t.type for t in p.args]
actions = [(a.name, a.precond, a.params, [e[1] for e in a.effects]) for a in robot_domain.operators]

operations = {}
possible_args = {}
for a in actions:
    print()
    action_name = a[0]
    action_preconditions = a[1]
    action_args = a[2]
    action_effects = a[3]
    operations[action_name] = []
    operations[action_name].append([str(arg.name) for arg in action_args])
    operations[action_name].append([str(arg.type) for arg in action_args])
    precond = {}
    for i in [str(prec) for prec in action_preconditions]:
        s = re.split('[(,)]', i)[:-1]
        precond[s[0]] = s[1:]
    operations[action_name].append(precond)
    pos_eff = {}
    for i in [str(eff) for eff in action_effects if eff.is_positive()]:
        s = re.split('[(,)]', i)[:-1]
        pos_eff[s[0]] = tuple(s[1:])
    operations[action_name].append(pos_eff)
    neg_eff = {}
    for i in [str(eff.predicate) for eff in action_effects if eff.is_negative()]:
        s = re.split('[(,)]', i)[:-1]
        neg_eff[s[0]] = tuple(s[1:])
    operations[action_name].append(neg_eff)

initial_state = list(robot_problem.init)

state = {}

for s in initial_state:
    literal = [x.strip() for x in re.split('[(,)]', s)[:-1]]
    pred = literal[0]
    args = literal[1:]
    state[pred] = state.get(pred, [])
    state[pred].append(tuple(args))

print(state)
print(operations)
print(arguments)

# Checker(state, actions)


# tyreworld_domain = parser.parse(path + 'tyreworld_domain.pddl')
# tyreworld_problem = parser.parse(path + 'tyreworld_problem.pddl')
# print(tyreworld_domain)
# print(tyreworld_problem)
