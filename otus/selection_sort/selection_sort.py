from typing import List


class SelectionSort:
    """
    Сортировка выбором

    Сложность - квадратичная. Не стабильный. Не адаптивный. Не онлайн.
    """

    def __init__(self, array):
        self.array: List = array
        self.array_length: int = len(self.array) - 1

    def find_max(self, index: int) -> int:
        """
        Нахождение индекса максимального числа
        """
        _max: int = index
        for i in range(index):
            if self.array[i] > self.array[_max]:
                _max = i
        return _max

    def swap(self, index1: int, index2: int) -> None:
        """
        Перемещение элементов
        """
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell

    def sorting(self) -> None:
        """
        Сортировка
        """
        for i in range(self.array_length):
            sort_border: int = self.array_length - i
            _max = self.find_max(sort_border)
            self.swap(sort_border, _max)
