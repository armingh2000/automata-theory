

class tm_state:


    def __init__(self, state_number, is_final):
        self.state_number = state_number
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, state2, tape_read, tape_write, move_direction):
        self.transitions[tape_read].append((state2, tape_write, move_direction))


