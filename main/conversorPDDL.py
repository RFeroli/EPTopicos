import re

class Conversor:
    def __init__(self, domain, problem):
        self.domain_file = domain
        self.problem_file = problem
        with open(self.domain_file, 'r') as f:
            self.parse_domain(f)

    def parse_domain(self, f):
        for line in f.readlines():
            line = line.strip()
            if re.match(r';.*', line) or line == '':
                continue
            print(line)
    def parse_problem(self, f):
        pass


path = '../in/'

Conversor(path + 'robot_domain.pddl','robot_problem.pddl')
Conversor(path + 'tyreworld_domain.pddl','tyreworld_problem.pddl')