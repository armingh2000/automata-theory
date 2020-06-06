

class tm_state:


    def __init__(self, state_number, is_final):
        self.state_number = state_number
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, state2, tape_read, tape_write, move_direction):
        self.transitions[tape_read].append((state2, tape_write, move_direction))


class tape:


    def __init__(self):
        self.tape = []
        self.current_index = 0

    def clear(self):
        self.tape = 0
        self.current_index = 0

    def add_word(self, word):
        self.tape = ['#'] + list(word) + ['#']
        self.current_index = 1

    def perform_transition(self, transition):
        self.tape[self.current_index] = transition[1]
        self.current_index = self.current_index + 1 if transition(2) == 'r' else self.transition - 1

    def show(self):
        return self.tape[:]

    def current_letter(self):
        return self.tape[self.current_index]

