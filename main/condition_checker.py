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
            print(action_name)
            print('--- args:')
            print([(t.name, t.type) for t in action_args])
            print('--- preconditions:')
            for prec in action_preconditions:
                print(re.split('[(,)]', str(prec))[:-1])
            print('--- effects:')
            print(action_effects)
            print()
        pass

    def next_states(self):
        pass