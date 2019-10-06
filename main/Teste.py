import os
from main.pddlparser import PDDLParser
from main.domain import Domain
from main.condition_checker import Checker
import re

path = '../in/'


robot_domain = PDDLParser().parse(path + 'robot_domain.pddl')
robot_problem = PDDLParser().parse(path + 'robot_problem.pddl')

print([p.name for p in robot_domain.predicates])
actions = [(a.name, a.precond, a.params, [e[1] for e in a.effects]) for a in robot_domain.operators]

initial_state = list(robot_problem.init)
print('Initial state:\n')

state = {}
for s in initial_state:
    literal = [x.strip() for x in re.split('[(,)]', s)[:-1]]
    pred = literal[0]
    args = literal[1:]
    state[pred] = state.get(pred, [])
    state[pred].append(tuple(args))
print(state)

Checker(state, actions)


# tyreworld_domain = parser.parse(path + 'tyreworld_domain.pddl')
# tyreworld_problem = parser.parse(path + 'tyreworld_problem.pddl')
# print(tyreworld_domain)
# print(tyreworld_problem)
