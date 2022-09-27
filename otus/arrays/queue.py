from typing import List, Any, Tuple


class QueueKnownProirity:
    """
    Очередь с известным приоритетом.

    Высший приоритет имеют меньшие числа.
    """

    def __init__(self, priority):
        self.priority: int = priority
        self.container_array: List[List[Any]] = [[] for _ in range(priority)]

    def dequeue(self) -> Any:
        """
        Удаление элемента
        """
        for i in range(len(self.container_array)):
            if self.container_array[i]:
                for j in range(len(self.container_array[i])):
                    res: Any = self.container_array[i][j]
                    del self.container_array[i][j]
                    return res
            continue

    def enqueue(self, priority: int, item: Any) -> None:
        """
        Добавление элемента
        """
        priority_array: List = self.container_array[priority]
        priority_array.append(item)


class QueueUnknownPriority:
    """
    Очередь с не известным приоритетом.

    Высший приоритет имеют буквы начала алфавита.
    """

    def __init__(self):
        self.array: List = []

    def dequeue(self) -> Any:
        """
        Удаление элемента
        """
        if self.array:
            for i in range(len(self.array)):
                res: Any = self.array[i]
                del self.array[i]
                return res

    def enqueue(self, priority_and_item: Tuple[str, Any]) -> None:
        """
        Добавление элемента
        """
        priority_and_item[0].lower()

        if not self.array:
            self.array.append(priority_and_item)
            return

        for i in range(len(self.array)):
            prio, _ = self.array[i]
            if priority_and_item[0] < prio:
                self.array.insert(i, priority_and_item)
                break
            if i == len(self.array) - 1:
                self.array.append(priority_and_item)
