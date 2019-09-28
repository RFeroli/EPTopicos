from pddlpy import pddl

robot = pddl.DomainProblem('in/robot_domain.pddl','in/robot_problem.pddl')
tyreworld = pddl.DomainProblem('in/tyreworld_domain.pddl','in/tyreworld_problem.pddl')


state = set(map(pddl.Atom.tuple, robot.initialstate()))

for op in robot.operators():
    for i in robot.ground_operator(op):
        if i.precondition_pos.issubset(state):
            print(state.union(i.precondition_pos))




