class fa_state:


    def __init__(self, state_number, is_final, is_trap):
        self.state_number = state_number
        self.is_final = is_final
        self.is_trap = is_trap
        self.transitions = {}

    def add_transition(self, state2, letter):
        self.transitions[letter].append(state2)

    def letter_transition(self, letter):
        return self.transitions[letter]

class fa:


    def __init__(self, number_of_states, letters, finals, traps):
        self.number_of_states = number_of_states
        self.states = []

        for i in range(number_of_states):
            is_trap = i in traps
            is_final = i in finals
            self.states.append(fa_state(i, is_final, is_trap))

        self.letters = letters
        self.initiate_letters()

    def initiate_letters(self):
        for state in self.states:
            for letter in self.letters:
                state.transitions[letter] = []

    def add_transition(self, start_state, end_state, letter):
        start_state.add_transition(end_state, letter)

    def word_check(self, word):
        temp = self.walk(word, self.states[0], 0)
        return temp[0] if temp[1] else False

    def walk(self, word, current_state, current_index):
        if current_index == len(word):
            if current_state.is_final:
                return [(current_index, current_state)], True
            for state in current_state.transitions['-']:
                if state.is_final:
                    return [(current_index, state)], True
            else: return [], False

        if word[current_index] in self.letters:
            if current_state.is_trap:
                if current_state.is_final:
                    return [(m, current_state) for m in range(current_index, len(word) + 1)]
                else:
                    return [], False

            for state in current_state.letter_transition(word[current_index]):
                res = self.walk(word, state, current_index + 1)
                if res[1]:
                    return res[0] + [(current_index, current_state)], True

            for state in current_state.letter_transition('-'):
                res = self.walk(word, state, current_index)
                if res[1]:
                    return res[0] + [(current_index, current_state)], True

            return [], False
        else:
            return [], False



def main():
    letters = input("Enter FA letters: ").split() + ['-']
    n_states = int(input("Enter number of states: "))
    final_states = list(map(int, input("Enter final states: ").split()))
    trap_states = list(map(int, input("Enter trap states(trap state is a state that has all letter transitions forwarding to itself): ").split()))
    new_fa = fa(n_states, letters, final_states, trap_states)
    n_transition = int(input("Enter number of transitions (each transition has 'one' letter): "))
    print("Use - in lambda transition")
    print("Enter transitions in format: 'start_state end_state letter' ")
    for i in range(n_transition):
        temp = input("Enter transition: ").split()
        new_fa.add_transition(new_fa.states[int(temp[0])], new_fa.states[int(temp[1])], temp[2])

    loop = True
    while loop:
        word = input("Enter a word: ")
        result = new_fa.word_check(word)
        if result != False:
            print("This word is in this fa's language")
            result.reverse()
            print_result(result, word)
        else:
            print("This word is NOT in this FA's language")
        loop = False if input("Do you want to continue?(y, n) : ") == 'n' else True

def print_result(steps, word):
    for step in steps:
        index = step[0]
        state = step[1].state_number
        print("current state: q{}".format(state))
        print(word)
        print((" "*(index)) + ".")

main()

