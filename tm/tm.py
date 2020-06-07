

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


class tm:

    
    def __init__(self, number_of_states, letters, finals):
        self.number_of_states = number_of_states
        self.final_states = finals
        self.letters = letters
        self.states = []
        for i in range(number_of_states):
            is_final = i in finals
            self.states.append(tm_state(i, is_final))

        self.tape = tape()
        self.initiate_letters()

    def initiate_letters(self):
        for state in self.states:
            for letter in self.letters:
                state.transitions[letter] = []

    def add_transition(self, start_state, end_state, tape_read, tape_write, move_direction):
        start_state.add_transition(end_state, tape_read, tape_write, move_direction)

    def performable_transition(self, transition):
        if self.tape.tape[self.tape.current_index] == transition[1]:
            return True
        return False

    def perform_transition(self, transition):
        self.tape.perform_transition(transition)

    def undo_transition(self, transition):
        self.tape.current_index = self.tape.current_index - 1 if transition[2] == 'r' else self.tape.current_index + 1
        self.tape[self.tape.current_index] = transition[1]

    def step(self, current_state):
        return (self.tape.current_index, current_state, self.tape.show())

    def word_check(self, word):
        self.tape.add_word(word)
        temp = self.walk(self.states[0])
        return temp[0] if temp[1] else temp[1]

    def halt_check(self, current_state):
        if len(current_state.transitions[self.tape.current_letter()]) == 0:
            return True
        return False

    def walk(self, current_state):
        if halt_check(current_state):
            if current_state.is_final:
                return [self.step(current_state)], True

            return [], False

        for transition in current_state.transitions[self.current_letter()]:
            if self.performable_transition(transition):
                self.perform_transition(transition)
                res = self.walk(transition[0])
                if res[1]:
                    return res[0] + [self.step(current_state)], True
                self.undo_transition(transition)
        return [], False



