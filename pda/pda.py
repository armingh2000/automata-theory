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

    def performable_transition(self, transition):
        if self.stack.stack[-1] == transition[1] or transition[1] == '-':
                return True

        return False

    def walk(self, word, current_state, current_index):
        if current_index == len(word):
            if current_state.is_final:
                return [(current_index, current_state, self.stack.show())], True
            for transition in current_state.transitions['-']:
                if transition[0] != current_state:
                    if self.performable_transition(transition):
                        self.perform_transition(transition)
                        res = self.walk(word, transition[0], current_index)
                        self.undo_transition(transition)
                        if res[1]:
                            return res[0] + [(current_index, current_state, self.stack.show())], True
            return [], False

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
                if self.performable_transition(transition):
                    self.perform_transition(transition)
                    res = self.walk(word, transition[0], current_index + 1)
                    self.undo_transition(transition)
                    if res[1]:
                        return res[0] + [(current_index, current_state, self.stack.show())], True

            for transition in current_state.transitions['-']:
                if self.performable_transition(transition):
                    self.perform_transition(transition)
                    res = self.walk(word, transition[0], current_index)
                    self.undo_transition(transition)
                    if res[1]:
                        return res[0] + [(current_index, current_state, self.stack.show())], True

            return [], False

        return [], False

def main():
    letters = input("Enter PDA letters: ").split() + ['-']
    n_states = int(input("Enter number of states: "))
    final_states = list(map(int, input("Enter final states: ").split()))
    trap_states = list(map(int, input("Enter trap states(trap state is a state that has all letter transitions forwarding to itself): ").split()))
    stack_variables = input("Enter stack variables: ").split() + ['-']
    new_pda = pda(n_states, letters, final_states, trap_states, stack_variables)
    n_transitions = int(input("Enter number of transitions(each transition has 'one' letter):"))
    print("Use - in lambda transition")
    print("Enter transitions in format: 'start_state end_state letter stack_pop_letter stack_push_letter' ")

    for i in range(n_transitions):
        temp = input("Enter transition: ").split()
        new_pda.add_transition(new_pda.states[int(temp[0])], new_pda.states[int(temp[1])], temp[2], temp[3], temp[4])

    loop = True

    while loop:
        word = input("Enter a word: ")
        result = new_pda.word_check(word)
        if result == False:
            print("This word is NOT in this PDA's language")
        else:
            print("This word is in this PDA's language")
            result.reverse()
            print_result(result, word)
        loop = False if input("Do you want to continue?(y, n): ") == 'n' else True


def print_result(steps, word):
    for step in steps:
        index = step[0]
        state = step[1].state_number
        stack = step[2]
        print("current state: q{}".format(state))
        print("stack: {}".format(stack))
        print(word)
        print((" "*(index)) + ".")


main()



