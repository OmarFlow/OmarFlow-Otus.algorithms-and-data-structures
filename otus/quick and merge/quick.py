from typing import List


class QuickSort:
    """
    Быстрая сортировка

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

    def sort(self, left, right) -> None:
        """
        Сортировка
        """
        if left >= right:
            return

        x = self.split(left, right)
        self.sort(left, x - 1)
        self.sort(x + 1, right)

    def split(self, left: int, right: int) -> int:
        """
        Разделение.

        В левой части элементы меньше опорного(pivot), в правой - больше.
        """
        pivot = self.array[right]
        m = left - 1

        for i in range(left, right + 1):
            if self.array[i] <= pivot:
                m += 1
                self.swap(m, i)
        return m

    def swap(self, index1: int, index2: int) -> None:
        """
        Перемещение элементов
        """
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell
