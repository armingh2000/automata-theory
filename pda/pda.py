
class pda_state:


    def __init__(self, state_number, is_final, is_trap):
        self.state_number = state_number
        self.is_final = is_final
        self.is_trap = is_trap
        self.transitions = {}

    def add_transition(self, state2, letter, stack_pop_letter, stack_push_letter):
        self.transitions[letter].append((state2, stack_pop_letter, stack_push_letter))

    

