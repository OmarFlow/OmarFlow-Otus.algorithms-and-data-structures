from collections import deque
from typing import List


class MergeSort:
    """
    Сортировка слиянием

    Сложность - nlogn. Не стабильный. Не адаптивный. Не онлайн.
    """

    def __init__(self, array: List):
        self.array: List = array

    def sorting(self) -> List:
        """
        Основной метод сортировки
        """
        self.sort(0, len(self.array) - 1)
        return self.array

    def sort(self, left: int, right: int) -> None:
        """
        Сортировка
        """
        if left >= right:
            return

        middle: int = (left + right) // 2

        self.sort(left, middle)
        self.sort(middle + 1, right)
        self.merge(left, middle, right)

    def merge(self, left: int, middle: int, right: int) -> None:
        """
        Слияние
        """
        container: deque = deque()
        a = left
        b = middle + 1

        while a <= middle and b <= right:
            if self.array[a] > self.array[b]:
                container.append(self.array[b])
                b += 1
            else:
                container.append(self.array[a])
                a += 1

        while a <= middle:
            container.append(self.array[a])
            a += 1

        while b <= right:
            container.append(self.array[b])
            b += 1

        for i in range(left, right + 1):
            self.array[i] = container.popleft()
