from typing import List
from random import choice
from copy import deepcopy, copy
from collections import defaultdict


class OrGraphNode:
    def __init__(self):
        self.incoming = []
        self.outgoing = []


class OrGraph:
    def __init__(self):
        self.graph = defaultdict(OrGraphNode)
        self.inverted_graph = None
        self.sorted_vertexes = []
        self.check_vertex_map = {}
        self.check_visited_map = {}
        self.strong_connectivity_component = []
        self.strong_connectivity_components = []

    def add_edge(self, from_vertex: int, to_vertex: int, direction: str) -> None:
        """
        Добавление ребра в граф
        """
        another_direction = "incoming" if direction == "outgoing" else "outgoing"
        getattr(self.graph[from_vertex], direction).append(to_vertex)
        getattr(self.graph[to_vertex], another_direction).append(from_vertex)

    def swap_arc(self, vertex: OrGraphNode) -> None:
        """
        Инвертирование дуг
        """
        buffer = vertex.outgoing
        vertex.outgoing = vertex.incoming
        vertex.incoming = buffer

    def make_invert_graph(self) -> None:
        """
        Инвертирование графа
        """
        graph = deepcopy(self.graph)
        for _, vertex in graph.items():
            self.swap_arc(vertex)
        self.inverted_graph = graph

    def kosarayu_algorithm(self) -> List[List[int]]:
        """
        Нахождение компонентов сильной связанности алгоритмом Косарайю
        """
        self.make_invert_graph()

        not_vivisted_vertexes = self.inverted_graph.keys() - self.check_vertex_map
        while len(not_vivisted_vertexes) != len(self.sorted_vertexes):
            self.traversal_inverted()
            self.check_visited_map.clear()

        while self.sorted_vertexes:
            self.traversal_original(self.sorted_vertexes[-1])
            self.sorted_vertexes = self.sorted_vertexes[:-len(self.strong_connectivity_component)]
            self.strong_connectivity_components.append(copy(self.strong_connectivity_component))
            self.strong_connectivity_component.clear()

        return self.strong_connectivity_components

    def traversal_inverted(self, key=None) -> None:
        """
        Обходим инвертированный граф
        """
        if key:
            vertex = self.inverted_graph[key]
        else:
            key, vertex = choice(list(self.inverted_graph.items()))
        self.check_visited_map[key] = True

        if vertex.outgoing:
            for key_ in vertex.outgoing:
                if key_ not in self.check_visited_map:
                    self.traversal_inverted(key_)

        if key not in self.check_vertex_map:
            self.sorted_vertexes.append(key)
            self.check_vertex_map[key] = True

        return

    def traversal_original(self, key=None) -> None:
        """
        Обходим первоначальный граф
        """
        vertex = self.graph[key]

        self.check_visited_map[key] = True

        if vertex.outgoing:
            for key_ in vertex.outgoing:
                if key_ not in self.check_visited_map:
                    self.traversal_original(key_)

        self.strong_connectivity_component.append(key)
        return


# g = OrGraph()
# g.add_edge(1, 2, "outgoing")
#
# g.add_edge(2, 3, "outgoing")
# g.add_edge(2, 6, "outgoing")
# g.add_edge(2, 5, "outgoing")
#
# g.add_edge(3, 7, "outgoing")
# g.add_edge(3, 4, "outgoing")
#
# g.add_edge(4, 3, "outgoing")
# g.add_edge(4, 8, "outgoing")
#
#
# g.add_edge(5, 1, "outgoing")
# g.add_edge(5, 6, "outgoing")
#
# g.add_edge(6, 7, "outgoing")
#
# g.add_edge(7, 6, "outgoing")
#
# g.add_edge(8, 4, "outgoing")
# g.add_edge(8, 7, "outgoing")