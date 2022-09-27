from typing import List


class HeapSort:
    """
    Пирамидальная сортировка

    Сложность - nlogn. Не стабильный. Не адаптивный. Не онлайн.
    """

    def __init__(self, array: List):
        self.array: List = array
        self.array_length: int = len(self.array)

    def swap(self, index1: int, index2: int) -> None:
        """
        Перемещение элементов
        """
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell

    def heapify(self, root: int, border: int) -> None:
        """
        Превращение массива в 'кучу'
        """
        left: int = 2 * root + 1
        right: int = left + 1

        x: int = root
        if border > left:
            x = left if self.array[left] > self.array[x] else x
        if border > right:
            x = right if self.array[right] > self.array[x] else x

        if x == root:
            return

        self.swap(x, root)
        self.heapify(x, border)

    def sorting(self) -> None:
        """
        Сортировка
        """
        for i in range(int(self.array_length / 2 - 1), -1, -1):
            self.heapify(i, self.array_length)

        for i in range(self.array_length - 1, 0, -1):
            self.swap(0, i)
            self.heapify(0, i)
