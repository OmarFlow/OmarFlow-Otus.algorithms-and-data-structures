from insert import optimized_insert_sort


def shell_sort(array):
    step = len(array) // 2
    while step > 2:
        for i in range(len(array)):
            if i + (step * 2) > len(array):
                step //= 2
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


def shell_sort_1(array):
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


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer

    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]

    for i in a, b, c:
        start = timer()
        shell_sort(i)
        end = timer()
        print(end - start)
