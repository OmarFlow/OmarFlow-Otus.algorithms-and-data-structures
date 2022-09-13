class QuickSort:
    def __init__(self, array):
        self.array = array

    def sorting(self):
        self.sort(0, len(self.array) - 1)
        return self.array

    def sort(self, left, right):
        if left >= right:
            return

        x = self.split(left, right)
        self.sort(left, x - 1)
        self.sort(x + 1, right)

    def split(self, left, right):
        pivot = self.array[right]
        m = left - 1

        for i in range(left, right + 1):
            if self.array[i] <= pivot:
                m += 1
                self.swap(m, i)
        return m

    def swap(self, index1, index2):
        cell = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = cell


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
        QuickSort(i).sorting()
        end = timer()
        print(end - start)
