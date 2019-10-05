class Action:
    def __init__(self,action):
        self.action_name = action[0]
        self.action_preconditions = action[1]
        self.action_args = action[2]
        self.action_effects = action[3]
        
    def get_Sprecond_instances(self, tuplaArg):
        variable_map = {}
        for i, j in zip (tuplaArg, self.action_args):
            variable_map[j.name] = i
            
        answer = []
        for precond in self.action_preconditions:
            string_predicate = str (precond)
            for arg_precond in precond.predicate.args:
                string_predicate = string_predicate.replace (arg_precond, variable_map[arg_precond])
            answer.append (string_predicate)

        return answer

    def check_precond(self, state,Spreconds):
        return all (s in state for s in Spreconds)
    
    def get_Sefects(self, tuplaArg):
        pares = {}
        for i, j in zip (tuplaArg,self.action_args):
            pares[j.name] = i
        positive_effects=[]
        negativeEffects=[]
        for efect in self.action_effects:
            predicate = str (efect)
            for arg_effect in efect.predicate.args:
                predicate = predicate.replace (arg_effect, pares[arg_effect])
            pass
            if efect._positive:
                positive_effects.append(predicate)
            else:
                predicate = predicate.replace ("not ", "")
                negativeEffects.append(predicate)
        return (positive_effects,negativeEffects)

    def agregate_Seffects(self, state, efects):
        # positivos
        for efect in efects[0]:
            state.append (efect)
         # negativos
        for efect in efects[1]:
             state.remove (efect)

    def perform(self,tuplaArg,state):
        state_clone=state[:]
        if self.check_precond(state_clone,self.get_Sprecond_instances(tuplaArg)):
            self.agregate_Seffects(state_clone,self.get_Sefects(tuplaArg))
            return state_clone
        else:
            return []

