import re

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

    def get_planner_args(self):
        return self.problem['init'], self.problem['goal'], self.domain['action'], self.problem['objects']

    def parse_domain(self, f):
        domain = ' '.join([line.strip() for line in f.readlines() if not re.match(r';.*', line) and line != '\n'])
        args = self.get(domain)
        for a in args:
            if re.match(r'[a-z]* [a-z0-9-]*$', a):
                self.domain['name'] = a.split(' ')[1]

            else:
                reg = re.search(r'([a-z]*) (.*)$', a)
                arg_type = reg.group(1)
                s = reg.group(2)
                if arg_type == 'requirements':
                    self.domain[arg_type] = self.parse_requirements(s)
                elif arg_type == 'types':
                    self.domain[arg_type] = self.parse_types(s)
                elif arg_type == 'constants':
                    self.domain[arg_type] = self.parse_constants(s)
                elif arg_type == 'predicates':
                    self.domain[arg_type] = self.parse_predicates(s)
                elif arg_type == 'action':
                    self.domain[arg_type] = self.domain.get(arg_type, {})
                    self.domain[arg_type].update(self.parse_action(s))
                else:
                    pass

    def get(self, s, for_level=1, i=0):
        level = 0
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
        return tree[for_level]


    def parse_problem(self, f):
        problem = ' '.join([line.strip() for line in f.readlines() if not re.match(r';.*', line) and line != '\n'])
        args = self.get(problem)
        for a in args:
            if re.match(r'[a-z]* [a-z0-9-]*$', a):
                self.problem['name'] = a.split(' ')[1]
            else:
                reg = re.search(r'([a-z]*) (.*)$', a)
                arg_type = reg.group(1)
                s = reg.group(2)
                if arg_type == 'domain':
                    self.problem[arg_type] = self.parse_problem_domain(s)
                elif arg_type == 'objects':
                    self.problem[arg_type] = self.parse_objects(s)
                elif arg_type == 'init' or arg_type == 'goal':
                    self.problem[arg_type] = self.parse_state(s)

    def parse_types(self, s):
        if '-' in s:
            all_types = []
            self.domain['has_hierarchy'] = True
            types = {}
            tl = []
            i = 0
            split_list = s.split(' ')
            while i < len(split_list):
                if split_list[i] == '-':
                    types[split_list[i + 1]] = types.get(split_list[i+1], [])
                    types[split_list[i+1]].extend(tl.copy())
                    tl = []
                    i += 1
                else:
                    all_types.append(split_list[i])
                    tl.append(split_list[i])
                i += 1
            self.domain['type_hierarchy'] = types
            return all_types
        else:
            self.domain['has_hierarchy'] = False
            return [e.strip() for e in s.split(' ') if e != '']


    def parse_requirements(self, s):
        return [req.strip().replace(':', '') for req in s.split(' ')]

    def parse_constants(self, s):
        constants = {}
        l = []
        i = 0
        split_list = s.split(' ')
        while i < len(split_list):
            if split_list[i] == '-':
                constants[split_list[i + 1]] = l.copy()
                l = []
                i += 1
            else:
                l.append(split_list[i])
            i += 1
        return constants

    def parse_predicates(self, s):
        predicates = {}
        if ' - ' in s:
            for p in self.get(s, for_level=0):
                a = p.split(' ')
                p_name = a[0].strip()
                j = 1
                predicates[p_name] = [[], []]
                while j < len(a):
                    predicates[p_name][0].append(a[j].strip())
                    predicates[p_name][1].append(a[j+2].strip())
                    j += 3
        else:
            for p in self.get(s, for_level=0):
                a = p.split(' ')
                p_name = a[0].strip()
                predicates[p_name] = [[x.strip() for x in a[1:]], []]
                predicates[p_name][1] = [None] * len(predicates[p_name][0])
        return predicates

    def parse_action(self, s):
        # print(s.strip())

        a = re.search(r'([a-z-]*) :parameters \(([?a-z- ]*)\) :precondition \(([?a-z- ()]*)\) :effect \([and ]{0,4}([?a-z- ()]*)\)$', s.strip())
        action_name = a.group(1)
        # variaveis, tipo, precondicoes, efeitos positivos e efeitos negativos
        action = {action_name:[[],[],{},{},{}]}
        params = a.group(2).split(' ')

        ls = []
        is_type = False
        for j in params:
            if j == '':
                continue
            if is_type:
                is_type = False
                action[action_name][0].extend(ls.copy())
                action[action_name][1].extend([j] * len(ls))
                ls = []
            elif j == '-':
                is_type = True
            else:
                ls.append(j)
        preconds = a.group(3)
        if 'and' in preconds:
             preconds = preconds[3:].strip()
        if not re.match(r'[()]', preconds):
            preconds = '({})'.format(preconds)
        for j in self.get(preconds, for_level=0):
            p = j.split(' ')
            action[action_name][2][p[0]] = action[action_name][2].get(p[0], [])
            action[action_name][2][p[0]].insert(0, p[1:])
        effects = self.get(a.group(4), for_level=0)
        for j in effects:
            e = j
            positive = 0
            match = re.search(r'not ?\(([a-z- ?]*)\)$', j)
            if match:
                positive = 1
                e = match.group(1)
            e = e.split(' ')
            action[action_name][3+positive][e[0]] = tuple(e[1:])
        return action

    def parse_problem_domain(self, s):
        return s.strip()

    def parse_objects(self, s):
        objects = {}
        obj_list = []
        is_type = False
        for arg in s.strip().split(' '):
            if is_type:
                is_type = False
                if self.domain['has_hierarchy'] and self.domain['type_hierarchy'].get(arg, False):
                    obj_list = []
                else:
                    objects[arg] = objects.get(arg, set())
                    objects[arg].update(set(obj_list.copy()))
                    obj_list = []
            elif arg == '-':
                is_type = True
            else:
                obj_list.append(arg)
        if self.domain['has_hierarchy']:
            for k,v in self.domain['type_hierarchy'].items():
                objects[k] = objects.get(k, set())
                for x in v:
                    objects[k].update(objects.get(x, set()))
        return objects

    def parse_state(self, s):
        state = {}
        for pred in re.findall(r'\(([a-z-0-9]*) ([a-z-0-9 ]*)\)', s.strip()):
            state[pred[0]] = state.get(pred[0], set())
            state[pred[0]].add(tuple(pred[1].split(' ')))
        return state

path = '../in/'

Conversor(path + 'tyreworld_domain.pddl', path + 'tyreworld_problem.pddl').get_planner_args()
for i in range(2,11):
    Conversor(path + 'robot_domain.pddl', path + 'robot_problem_{}b.pddl'.format(i)).get_planner_args()
