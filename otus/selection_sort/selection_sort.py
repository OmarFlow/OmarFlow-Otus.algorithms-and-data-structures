class SelectionSort:
    """
    Сортировка выбором
    """

    def __init__(self, array):
        self.array = array
        self.array_length = len(self.array) - 1

    def find_max(self, index):
        max = index
        for i in range(index):
            if self.array[i] > self.array[max]:
                max = i
        return max

    def swap(self, index1, index2):
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell

    def sorting(self):
        for i in range(self.array_length):
            sort_border = self.array_length - i
            max = self.find_max(sort_border)
            self.swap(sort_border, max)


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer

    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]

    for i in a, b, c, d, e:
        ss = SelectionSort(i)
        start = timer()
        ss.sorting()
        end = timer()
        print(end - start)
