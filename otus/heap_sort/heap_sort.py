class HeapSort:
    """
    Пирамидальная сортировка
    """
    def __init__(self, array):
        self.array = array
        self.array_length = len(self.array)

    def swap(self, index1, index2):
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell

    def heapify(self, root, border):
        left = 2 * root + 1
        right = left + 1

        x = root
        if border > left:
            x = left if self.array[left] > self.array[x] else x
        if border > right:
            x = right if self.array[right] > self.array[x] else x

        if x == root:
            return

        self.swap(x, root)
        self.heapify(x, border)

    def sorting(self):
        for i in range(int(self.array_length / 2 - 1), -1, -1):
            self.heapify(i, self.array_length)

        for i in range(self.array_length - 1, 0, -1):
            self.swap(0, i)
            self.heapify(0, i)


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer
    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]

    for i in a, b, c, d, e:
        hh = HeapSort(i)
        start = timer()
        hh.sorting()
        end = timer()
        print(end - start)