import re
import pyparsing

class Conversor:

    def __init__(self, domain, problem):
        self.domain = {}
        self.problem = {}
        self.domain_file = domain
        self.problem_file = problem
        with open(self.domain_file, 'r') as f:
            self.parse_domain(f)
        with open(self.problem_file, 'r') as f:
            self.parse_problem(f)

    def parse_domain(self, f):
        domain = ' '.join([line.strip() for line in f.readlines() if not re.match(r';.*', line) and line != '\n'])
        args = self.get(domain)
        print(args)

    def get(self, s, level=0, i=0):
        tree = {}
        token = []
        opener = {}
        while i < len(s):
            if s[i] == '(':
                opener[level] = i
                level += 1
            elif s[i] == ')':
                level -= 1
                tree[level] = tree.get(level, [])
                tree[level].append(s[opener[level]+1:i])
            i += 1
        return tree[1]


    def parse_problem(self, f):
        problem = ' '.join([line.strip() for line in f.readlines() if not re.match(r';.*', line) and line != '\n'])
        args = self.get(problem)
        print(args)


path = '../in/'

Conversor(path + 'robot_domain.pddl', path + 'robot_problem.pddl')
Conversor(path + 'tyreworld_domain.pddl', path + 'tyreworld_problem.pddl')