from algoritmo_busca.busca import Busca
from main.planejador import Estado, Planejador
from main.conversorPDDL import Conversor
import time

nome_heuristica = {'um': 'retorna 1', 'soma': 'soma de níveis', 'max': 'nível máximo','FF':"fast forward"}

# problema do robo e problema tyreworld
problemas = [('tyreworld_domain.pddl', 'tyreworld_problem.pddl', 'Problema TyreWorld')]
# Heurísticas que retorna 1, soma de nível, máximo nível e fast foward
heuristicas = ['soma']

path = '../in/'
saida_estatisticas = '../estatisticas/saida_problema.txt'
saida_planos = '../estatisticas/saida_planos.txt'
estatisticas = {'Problema TyreWorld': {'um':[], 'soma': [], 'max': [], 'FF':[]}}

estado_atual = {"in":  {('pump', 'boot')},
"unlocked":  {('boot',)},
"intact":  {('r1',)},
"not-inflated":  {('r1',)},
"open":  {('boot',)},
"have":  {('nuts1',), ('wrench',), ('w1',)},
"not-on-ground":  {('the-hub1',)},
"unfastened":  {('the-hub1',)},
"on":  {('r1', 'the-hub1')}}


for problema in problemas:
    estado, meta, operacoes, argumentos = Conversor(path + problema[0], path + problema[1]).get_planner_args()
    pl = Planejador(argumentos, operacoes, Estado(estado), Estado(meta), 'soma')
    for es in pl.vizinhos(Estado(estado_atual)):
        print(es.dict)
        print(es.operacao)
        print('----')



