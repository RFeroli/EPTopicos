import os
from main.parser import PDDL_Parser

path = '../in/'
print(os.listdir(path))

p = PDDL_Parser()
p.parse_domain(path+"robot_domain.pddl")