
class pda_state:


    def __init__(self, state_number, is_final, is_trap):
        self.state_number = state_number
        self.is_final = is_final
        self.is_trap = is_trap
        self.transitions = {}

    def add_transition(self, state2, letter, stack_pop_letter, stack_push_letter):
        self.transitions[letter].append((state2, stack_pop_letter, stack_push_letter))


class stack:


    def __init__(self, stack_variables):
        self.stack = []
        self.stack_variables = stack_variables
        self.stack.append("$")

    def push(self, letter):
        if letter != '-':
            self.stack.append(letter)

    def pop(self, letter):
        if letter != '-':
            if letter != self.stack[-1]:
                self.stack.pop(-1)

    def show(self):
        return self.stack[:]


class pda:


    def __init__(self, number_of_states, letters, finals, traps, stack_variables):
        self.number_of_states = number_of_states
        self.letters = letters
        self.final_states = finals
        self.trap_states = traps
        self.stack = stack(stack_variables)
        self.states = []
        
        for i in range(number_of_states):
            is_final = i in finals
            is_trap = i in traps
            self.states.append(pda_state(i, is_final, is_trap))
    
        self.initiate_letters()

    def initiate_letters(self):
        for state in self.states:
            for letter in self.letters:
                state.transitions[letter] = []

    def add_transition(self, start_state, end_state, letter, pop_stack, push_stack):
        start_state.add_transition(end_state, letter, pop_stack, push_stack)

    def word_check(self, word):
        temp = self.walk(word, self.states[0], 0)
        return temp[0] if temp[1] else False

    def perform_transition(self, transition):
        self.stack.pop(transition[1])
        self.stack.push(transition[2])

    def undo_transition(self, transition):
        self.stack.pop(transition[2])
        self.stack.push(transition[1])

    def walk(self, word, current_state, current_index):
        if current_index == len(word):
            if current_state.is_final:
                return [(current_index, current_state, self.stack.show())], True
        if word[current_index] in self.letters:
            if current_state.is_trap:
                if current_state.is_final:
                    res = []
            
                    for i in range(current_index, len(word)):
                        res.append((i, current_state, self.stack.show()))
                        self.perform_transition(current_state.transitions[word[i]])
                        
                    res.append((len(word), current_state, self.stack.show()))
                    return res, True
               
                else:
                    return [], False
            
            for transition in current_state.transitions[word[current_index]]:
                if self.stack.stack[-1] == transition[1]:
                    self.stack.perform_transition(transition)
                    res = self.walk(word, transition[0], current_index + 1)
                    if res[1]:
                        return res[0].append((current_index, current_state, self.stack.show())), True
                    else:
                        self.undo_transition(transition)
                
            for transition in current_state.transitions('-'):
                if self.stack.stack[-1] == transition[1]:
                    self.stack.perform_transition(transition)
                    res = self.walk(word, transition[0], current_index) 
                    if res[1]:
                        return res[0].append((current_index, current_state, self.stack.show())), True
                    else:
                        self.undo_transition(transition)

            return [], False





