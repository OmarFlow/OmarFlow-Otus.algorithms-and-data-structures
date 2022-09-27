from typing import List, Optional, Any


def insert_sort(array: List) -> List:
    """
    Сортировка вставкой

    Сложность - квадратичная. Стабильный. Адаптивный. Онлайн.
    """
    for i in range(1, len(array)):
        j = i - 1
        while j >= 0 and array[j] > array[j + 1]:
            m = array[j + 1]
            array[j + 1] = array[j]
            array[j] = m
            j -= 1
    return array


def binary_search(num: int, mas: List) -> Optional[int]:  # type: ignore
    """
    Бинарный поиск индекса для вставки
    """
    low = 0
    high = len(mas) - 1
    if num <= mas[0]:
        return 0
    if num >= mas[-1]:
        return len(mas) - 1

    while low <= high:
        mid: int = (low + high) // 2
        if mas[mid - 1] <= num <= mas[mid + 1]:
            if num > mas[mid]:
                return mid + 1
            return mid

        if num > mas[mid]:
            low = mid + 1

        if num < mas[mid]:
            high = mid - 1


def optimized_insert_sort(array: List) -> List:
    """
    Нахождение индекса вставки в отсортированную часть за логарифмическое время
    """
    for i in range(1, len(array)):
        j = i - 1
        sorted_part: List = array[:i]
        if len(sorted_part) < 3:
            while j >= 0 and array[j] > array[j + 1]:
                m = array[j + 1]
                array[j + 1] = array[j]
                array[j] = m
                j -= 1
        else:
            k: Optional[int] = binary_search(array[i], sorted_part)
            value: Any = array[i]
            del array[i]
            array.insert(k, value)  # type: ignore
    return array
