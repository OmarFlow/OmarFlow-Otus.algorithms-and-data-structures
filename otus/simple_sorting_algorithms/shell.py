from typing import List

from insert import optimized_insert_sort


def shell_sort(array: List) -> List:
    """
    Шэл сортировка

    Сложность - чуть быстрее квадратичной. Не стабильный. Не адаптивный. Не онлайн.
    """
    step: int = len(array) // 2
    while step > 2:
        for i in range(len(array)):
            if i + (step * 2) > len(array):
                step //= 2
                break

            current_index = step + i
            res_items: List = [array[i]]
            res_indexes: List = [i]
            while current_index <= len(array) - 1:
                res_items.append(array[current_index])
                res_indexes.append(current_index)
                current_index += step

            sorted_res_items = optimized_insert_sort(res_items)
            for index, item in zip(res_indexes, sorted_res_items):
                array[index] = item
    return optimized_insert_sort(array)


def shell_sort_1(array):
    """
    Вариация выбора шага
    """
    step = 1
    step_power = 2
    while step > 2:
        for i in range(len(array)):
            if i + (step * 2) > len(array):
                step *= step_power * step_power - 1
                step_power *= step_power
                break

            current_index = step + i
            res_items = [array[i]]
            res_indexes = [i]
            while current_index <= len(array) - 1:
                res_items.append(array[current_index])
                res_indexes.append(current_index)
                current_index += step

            sorted_res_items = optimized_insert_sort(res_items)
            for index, item in zip(res_indexes, sorted_res_items):
                array[index] = item
    optimized_insert_sort(array)


def shell_sort_2(array):
    """
    Вариация выбора шага
    """
    step = 2
    while step > 2:
        for i in range(len(array)):
            if i + (step * 2) > len(array):
                step *= step + 1
                break

            current_index = step + i
            res_items = [array[i]]
            res_indexes = [i]
            while current_index <= len(array) - 1:
                res_items.append(array[current_index])
                res_indexes.append(current_index)
                current_index += step

            sorted_res_items = optimized_insert_sort(res_items)
            for index, item in zip(res_indexes, sorted_res_items):
                array[index] = item
    optimized_insert_sort(array)
