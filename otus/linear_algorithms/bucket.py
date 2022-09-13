from otus.simple_sorting_algorithms.bubble import bubble_sort


class SortArray:
    def __init__(self):
        self.array = []

    def append(self, item):
        self.array.append(item)
        if len(self.array) > 1:
            self.array = bubble_sort(self.array)


class BucketSort:
    def __init__(self, array):
        self.array = array
        self.max = self.find_max() + 1
        self.len = len(array)
        self.work_array = [SortArray() for _ in range(len(self.array))]
        self.result_array = []

    def find_max(self):
        max = 0
        for i in self.array:
            if i > max:
                max = i
        return max

    def sorting(self):
        for i in self.array:
            index = i * self.len // self.max
            self.work_array[index].append(i)

        for i in self.work_array:
            self.result_array.extend(i.array)


if __name__ == "__main__":
    from random import randint
    from timeit import default_timer as timer

    a = [randint(1, 1000000) for _ in range(100)]
    b = [randint(1, 1000000) for _ in range(1000)]
    c = [randint(1, 1000000) for _ in range(10000)]
    d = [randint(1, 1000000) for _ in range(100000)]
    e = [randint(1, 1000000) for _ in range(1000000)]

    for i in a, b, c, d, e:
        ss = BucketSort(i)
        start = timer()
        ss.sorting()
        end = timer()
        print(end - start)
