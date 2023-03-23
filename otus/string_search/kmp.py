from typing import Optional, List


class KMP:
    """
    Поиск подстрок, методом Кнута-Морриса-Пратта
    """
    class State:
        def __init__(self, wait: str):
            self.wait = wait
            self.next: Optional['KMP.State'] = None

    def __init__(self):
        self.initial_state = None
        self.current_state = None
        self.states =[]

    def search(self, text: str, pattern: str) -> Optional[List[int]]:
        # собираем состояния, указывая условия перехода и следующие состояние
        initial_state = self.State(pattern[0])
        self.current_state = initial_state
        self.initial_state = initial_state
        previous = initial_state
        for letter in pattern[1:]:
            state = self.State(letter)
            previous.next = state
            previous = state
            self.states.append(self.State(letter))

        # если получаемая буква ожидается, проходим на слежующие состояние, иначе переходим в начало
        start = 0
        finish = len(pattern)
        all_match = []
        for ind, letter in enumerate(text):
            if letter != self.current_state.wait:
                start = 0
                self.current_state = self.initial_state
            else:
                start += 1
                if start == finish:
                    all_match.append(ind - len(pattern) + 1)
                    self.current_state = self.initial_state
                    srart_ind = 0
                    continue
                self.current_state = self.current_state.next
        return all_match
