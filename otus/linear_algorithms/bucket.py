from typing import List, Any

from otus.simple_sorting_algorithms.bubble import bubble_sort


class SortArray:
    """
    Массив для блочной сортировки.

    Автоматически сортирует блок.
    """

    def __init__(self):
        self.array: List = []

    def append(self, item: Any) -> None:
        self.array.append(item)
        if len(self.array) > 1:
            self.array = bubble_sort(self.array)


class BucketSort:
    """
    Блочная сортировка

    Сложность - n. Стабильный. Не адаптивный. Онлайн, если известен максимальный элеменет.
    """

    def __init__(self, array: List):
        self.array: List = array
        self.max: int = self.find_max() + 1
        self.len: int = len(array)
        self.work_array: List[SortArray] = [SortArray()
                                            for _ in range(len(self.array))]
        self.result_array: List = []

    def find_max(self) -> int:
        """
        Нахождение максимального числа
        """
        max = 0
        for i in self.array:
            if i > max:
                max = i
        return max

    def sorting(self) -> None:
        """
        Сортировка
        """
        for i in self.array:
            index = i * self.len // self.max
            self.work_array[index].append(i)

        for i in self.work_array:
            self.result_array.extend(i.array)
