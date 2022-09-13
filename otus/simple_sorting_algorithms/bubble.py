def bubble_sort(array):
    """
    Сортировка пузырьком
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
        bubble_sort(i)
        end = timer()
        print(end - start)
