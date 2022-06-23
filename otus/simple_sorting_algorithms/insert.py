def insert_sort(array):
    for i in range(1, len(array)):
        j = i - 1
        while j >= 0 and array[j] > array[j+1]:
            m = array[j+1]
            array[j+1] = array[j]
            array[j] = m
            j -= 1
    return array


def binary_search(num, mas):
    low = 0
    high = len(mas) - 1
    if num <= mas[0]:
        return 0
    if num >= mas[-1]:
        return len(mas) - 1

    while low <= high:
        mid = (low + high) // 2
        if mas[mid - 1] <= num <= mas[mid + 1]:
            if num > mas[mid]:
                return mid + 1
            return mid

        if num > mas[mid]:
            low = mid + 1

        if num < mas[mid]:
            high = mid - 1


def optimized_insert_sort(array):
    for i in range(1, len(array)):
        j = i - 1
        sorted_part = array[:i]
        if len(sorted_part) < 3:
            while j >= 0 and array[j] > array[j + 1]:
                m = array[j + 1]
                array[j + 1] = array[j]
                array[j] = m
                j -= 1
        else:
            k = binary_search(array[i], sorted_part)
            value = array[i]
            del array[i]
            array.insert(k, value)
    return array


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer
    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]

    for i in a, b, c, d, e:
        start = timer()
        optimized_insert_sort(i)
        end = timer()
        print(end - start)

