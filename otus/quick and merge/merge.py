from collections import deque


class MergeSort:
    def __init__(self, array):
        self.array = array

    def sorting(self):
        self.sort(0, len(self.array) - 1)
        return self.array

    def sort(self, left, right):
        if left >= right:
            return

        middle = (left + right) // 2

        self.sort(left, middle)
        self.sort(middle + 1, right)
        self.merge(left, middle, right)

    def merge(self, left, middle, right):
        container = deque()
        a = left
        b = middle + 1

        while a <= middle and b <= right:
            if self.array[a] > self.array[b]:
                container.append(self.array[b])
                b += 1
            else:
                container.append(self.array[a])
                a += 1

        while a <= middle:
            container.append(self.array[a])
            a += 1

        while b <= right:
            container.append(self.array[b])
            b += 1

        for i in range(left, right + 1):
            self.array[i] = container.popleft()


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
        MergeSort(i).sorting()
        end = timer()
        print(end - start)
