from collections import defaultdict
from random import choice


class OrGraphNode:
    def __init__(self):
        self.incoming = []
        self.outgoing = []


class OrGraph:
    def __init__(self):
        self.graph = defaultdict(OrGraphNode)
        self.sorted_vertexes = []
        self.check_vertex_map = {}

    def add_edge(self, from_vertex: int, to_vertex: int, direction: str) -> None:
        """
        Добавление ребра в граф
        """
        another_direction = "incoming" if direction == "outgoing" else "outgoing"
        getattr(self.graph[from_vertex], direction).append(to_vertex)
        getattr(self.graph[to_vertex], another_direction).append(from_vertex)

    def taryan_sorting(self) -> None:
        not_vivisted_vertexes = self.graph.keys() - self.check_vertex_map
        while len(not_vivisted_vertexes) != len(self.sorted_vertexes):
            self.sort()
        return self.sorted_vertexes

    def sort(self, key=None) -> None:
        """
        Топологическая сортировка Тарьяна
        """
        if key:
            vertex = self.graph[key]
        else:
            key, vertex = choice(list(self.graph.items()))

        if vertex.outgoing:
            for vertex in vertex.outgoing:
                self.sort(vertex)

        if key not in self.check_vertex_map:
            self.sorted_vertexes.append(key)
            self.check_vertex_map[key] = True
        return
