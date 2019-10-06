import re
from main.stringMode import SAction

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

            string_action=SAction.Action(a)
            print("ESTADO SUCESSOR:",string_action.perform(tuplaArg=("room2","room1","blabla"),state=["robot-at(room1)"]))

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

