from typing import List
from random import choice
from collections import defaultdict


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

    def taryan_sorting(self) -> List[int]:
        """
        Топологическая сортировка Тарьяна
        """
        not_vivisted_vertexes = self.graph.keys() - self.check_vertex_map
        while len(not_vivisted_vertexes) != len(self.sorted_vertexes):
            self.traversal_graph()
        return self.sorted_vertexes

    def traversal_graph(self, key=None) -> None:
        """
        Обход графа
        """
        if key:
            vertex = self.graph[key]
        else:
            key, vertex = choice(list(self.graph.items()))

        if vertex.outgoing:
            for key_ in vertex.outgoing:
                self.traversal_graph(key_)

        if key not in self.check_vertex_map:
            self.sorted_vertexes.append(key)
            self.check_vertex_map[key] = True
        return
