import re

class Checker:
    def __init__(self, state, actions):
        print()
        self.current_state = state
        self.actions = actions
        for a in self.actions:
            action_name = a[0]
            action_preconditions = a[1]
            action_args = a[2]
            action_effects = a[3]

            self.testaPrecond(("banana","cafe","rainer"),action_args,action_preconditions,"")
            print(action_name)
            print('--- args:')
            print([(t.name, t.type) for t in action_args])
            print('--- preconditions:')
            for prec in action_preconditions:
                print(re.split('YYY', str(prec)))
            print('--- effects:')
            print(str(action_effects[0]))
            print()
        pass

    def testaPrecond(self,tuplaArg,args,preconds,state):

        pares={}
        for i,j in zip(tuplaArg,args):
            pares[j.name]=i

        for precond in preconds:
            predicado=str(precond)
            for argPrecond in precond.predicate.args:
                predicado=predicado.replace(argPrecond,pares[argPrecond])
            pass
            print("PREDICADO:",predicado)

        #TODO DEVOLVE VERDADEIRO SE O ESTADO CONTEM TODOS

    def getEfects(self, tuplaArg, args, preconds, state):

        pares = {}
        for i, j in zip (tuplaArg, args):
            pares[j.name] = i

        for precond in preconds:
            predicado = str (precond)
            for argPrecond in precond.predicate.args:
                predicado = predicado.replace (argPrecond, pares[argPrecond])
            pass
            print ("PREDICADO:", predicado)

        # TODO DEVOLVE VERDADEIRO SE O ESTADO CONTEM TODOS

    def next_states(self):
        pass