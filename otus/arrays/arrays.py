import copy
from copy import deepcopy
from abc import ABC, abstractmethod
from typing import List, Any, Tuple


class ArrayMixin(ABC):
    """
    Набор часто-используемой логики массива
    """

    def __init__(self):
        self.array: List[Any] = []

    def add(self, item: Any, index: int) -> None:
        """
        Добавление элемента в определённый индекс
        """
        self.resize()
        before_index = [self.array[i] for i in range(index)]
        before_index.append(item)

        for i in range(index, len(self.array)):
            before_index.append(self.array[i])

        self.array = before_index

    def get(self, index: int) -> Any:
        """
        Получение элемента
        """
        return self.array[index]

    def put(self, element: Any) -> None:
        """
        Добавление элемента в конец
        """
        self.resize()
        self.array[self.size] = element

    def remove(self, index: int) -> int:
        """
        Удаление элемента
        """
        deleted_item = self.array[index]
        del self.array[index]
        self.array.append(None)
        self.resize()
        return deleted_item

    @property
    def length(self) -> int:
        return len(self.array)

    @property
    def size(self) -> int:
        return sum(1 if i is not None else 0 for i in self.array)

    @abstractmethod
    def resize(self) -> None:
        """
        Расширение массива
        """
        ...


class SingleArray(ArrayMixin):
    """
    Единичый массив.

    При расширении увеличивает размер на 1.
    """

    def resize(self) -> None:
        # имитация расширения массива
        if self.array:
            self.array = deepcopy(self.array)

    def put(self, element: Any) -> None:
        self.resize()
        self.array.append(element)

    def remove(self, index: int) -> Any:
        deleted_item = self.array[index]
        del self.array[index]
        return deleted_item


class VectorArray(ArrayMixin):
    """
    Векторный массив.

    При расширении увеличивает размер на размер вектора.
    """

    def __init__(self, vector: int):
        self.array: List[Any] = [None for _ in range(vector)]
        self.vector: int = vector

    def resize(self) -> None:
        # имитация расширения массива
        if self.length == self.size:
            self.array = deepcopy(self.array)
            for i in range(self.vector):
                self.array.append(None)
        # уменьшение массива
        if self.length - self.size > self.vector:
            del self.array[-self.vector:]

    def add(self, item, index) -> None:
        super().add(item, index)
        del self.array[-1]


class FactorArray(VectorArray):
    """
    Факторный массив.

    При расширении увеличивает размер на текущий размер массива.
    """

    def __init__(self, array_size: int):
        self.array_size = array_size
        self.array = [None for _ in range(array_size)]

    def resize(self) -> None:
        # имитация расширения массива
        if self.length == self.size:
            self.array = deepcopy(self.array)
            self.array.extend([None for _ in range(self.length)])
        # уменьшение массива
        if self.length > self.array_size:
            if self.length - self.size > int(self.length / 2):
                del self.array[int(-(self.length / 2)):]


class MatrixArray:
    """
    Матричный массив.

    При расширении добавляет новый массив.
    """

    def __init__(self, array_size):
        self.array_size: int = array_size
        self.current_container_array_index: int = 0
        self.container_array: List = [[None for _ in range(array_size)]]

    def resize(self, specific_array: int = None) -> None:
        if specific_array:
            if self.is_empty_array(specific_array):
                del self.container_array[specific_array]
                self.current_container_array_index -= 1

        if self.current_array_size == self.array_size and not specific_array:
            self.current_container_array_index += 1
            self.container_array.append([None for _ in range(self.array_size)])

    def put(self, element: Any) -> None:
        """
        Добавление элемента в конец
        """
        self.resize()
        self.current_array[self.current_array_size] = element

    def get(self, index: int) -> Any:
        """
        Получение элемента
        """
        outer, inner = self.get_indexes(index)
        return self.container_array[outer][inner]

    def remove(self, index: int) -> Any:
        """
        Удаление элемента
        """
        outer, inner = self.get_indexes(index)
        element: Any = self.get(index)

        del self.container_array[outer][inner]
        self.container_array[outer].append(None)
        self.resize(outer)
        return element

    def add(self, item: Any, index: int) -> None:
        """
        Добавление элемента в определенный индекс
        """
        outer, inner = self.get_indexes(index)
        container_array_copy: List = copy.deepcopy(self.container_array)
        self.container_array: List = [  # type: ignore
            [None for _ in range(self.array_size)]]
        self.current_container_array_index = 0

        for i in range(len(container_array_copy)):
            for j in range(len(container_array_copy[i])):
                if i == outer and j == inner:
                    if container_array_copy[i][j] is None:
                        self.container_array[i][j] = item
                        break
                    self.put(item)
                self.put(container_array_copy[i][j])

    def is_empty_array(self, array_index: int) -> bool:
        return all(i is None for i in self.container_array[array_index])

    def get_indexes(self, index: int) -> Tuple[int, int]:
        """
        Внтуренний и внешний индекс
        """
        return index // self.array_size, index % self.array_size

    @property
    def current_array(self) -> List:
        """
        Текущий массив
        """
        return self.container_array[self.current_container_array_index]

    @property
    def current_array_size(self) -> int:
        """
        Размер текущего массива
        """
        return sum(1 if i is not None else 0 for i in self.current_array)
