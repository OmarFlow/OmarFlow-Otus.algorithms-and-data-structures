import copy
from copy import deepcopy
from abc import ABC, abstractmethod


class ArrayAddMixin(ABC):
    def __init__(self):
        self.array = []

    def add(self, item, index):
        self.resize()
        before_index = [self.array[i] for i in range(index)]
        before_index.append(item)

        for i in range(index, len(self.array)):
            before_index.append(self.array[i])

        self.array = before_index

    def get(self, index):
        return self.array[index]

    def put(self, element):
        self.resize()
        self.array[self.size] = element

    def remove(self, index):
        deleted_item = self.array[index]
        del self.array[index]
        self.array.append(None)
        self.resize()
        return deleted_item


    @property
    def length(self):
        return len(self.array)

    @property
    def size(self):
        return sum(1 if i is not None else 0 for i in self.array)

    @abstractmethod
    def resize(self):
        ...


class SingleArray(ArrayAddMixin):
    def __init__(self):
        super().__init__()

    def resize(self):
        if self.array:
            self.array = deepcopy(self.array)

    def put(self, element):
        self.resize()
        self.array.append(element)

    def remove(self, index):
        deleted_item = self.array[index]
        del self.array[index]
        return deleted_item


class VectorArray(ArrayAddMixin):
    def __init__(self, vector):
        self.array = [None for _ in range(vector)]
        self.vector = vector

    def resize(self):
        if self.length == self.size:
            self.array = deepcopy(self.array)
            for i in range(self.vector):
                self.array.append(None)
        if self.length - self.size > self.vector:
            del self.array[-self.vector:]

    def add(self, item, index):
        super().add(item, index)
        del self.array[-1]


class FactorArray(ArrayAddMixin):
    def __init__(self, array_size):
        self.array_size = array_size
        self.array = [None for _ in range(array_size)]

    def resize(self):
        if self.length == self.size:
            self.array = deepcopy(self.array)
            self.array.extend([None for _ in range(self.length)])
        if self.length > self.array_size:
            if self.length - self.size > int(self.length/2):
                del self.array[int(-(self.length/2)):]

    def add(self, item, index):
        super().add(item, index)
        del self.array[-1]


class MatrixArray:
    def __init__(self, array_size):
        self.array_size = array_size
        self.current_container_array_index = 0
        self.container_array = [[None for _ in range(array_size)]]

    def resize(self, specific_array=None):
        if specific_array:
            if self.is_empty_array(specific_array):
                del self.container_array[specific_array]
                self.current_container_array_index -= 1

        if self.size == self.array_size and not specific_array:
            self.current_container_array_index += 1
            self.container_array.append([None for _ in range(self.array_size)])

    def put(self, element):
        self.resize()
        self.current_array[self.size] = element

    def get(self, index):
        outer, inner = self.get_indexes(index)
        return self.container_array[outer][inner]

    def remove(self, index):
        outer, inner = self.get_indexes(index)
        element = self.get(index)

        del self.container_array[outer][inner]
        self.container_array[outer].append(None)
        self.resize(outer)
        return element

    def add(self, item, index):
        outer, inner = self.get_indexes(index)
        container_array_copy = copy.deepcopy(self.container_array)
        self.container_array = [[None for _ in range(self.array_size)]]
        self.current_container_array_index = 0

        for i in range(len(container_array_copy)):
            for j in range(len(container_array_copy[i])):
                if i == outer and j == inner:
                    if container_array_copy[i][j] is None:
                        self.container_array[i][j] = item
                        break
                    self.put(item)
                self.put(container_array_copy[i][j])

    def is_empty_array(self, array_index):
        return all(i is None for i in self.container_array[array_index])

    def get_indexes(self, index):
        return index // self.array_size, index % self.array_size

    @property
    def current_array(self):
        return self.container_array[self.current_container_array_index]

    @property
    def size(self):
        return sum(1 if i is not None else 0 for i in self.container_array[self.current_container_array_index])


if __name__ == "__main__":
    from timeit import default_timer as timer
    x = MatrixArray(10)
    for i in [1000, 10000, 100000, 1000000]:
        start = timer()
        for j in range(i):
            x.add(j, 0)
        end = timer()
        time_res = end - start
        print(f"data - {i}, elapsed time - {time_res}")
