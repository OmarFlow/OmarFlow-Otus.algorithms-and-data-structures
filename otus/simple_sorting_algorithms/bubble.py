from typing import List


def bubble_sort(array: List) -> List:
    """
    Сортировка пузырьком

    Сложность - квадратичная. Стабильный. Адаптивный. Не онлайн.
    """
    for i in range(len(array)):
        swapped = False
        for j in range(len(array) - i):
            try:
                if array[j] > array[j + 1]:
                    m = array[j + 1]
                    array[j + 1] = array[j]
                    array[j] = m
                    swapped = True
            except IndexError:
                continue
        if not swapped:
            break
    return array
