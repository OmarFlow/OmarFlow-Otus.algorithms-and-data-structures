from typing import List
from random import choice
from dataclasses import dataclass
from collections import defaultdict, namedtuple


class WeightedGraphNode:
    """
    Вершина/нода графа
    """
    def __init__(self):
        self.adjacent_vertices = []


@dataclass
class TableOfShortestPathsItem:
    weight: float
    key: int
    vertex: WeightedGraphNode


class WeightedGraph:
    """
    Взвешенный граф
    """
    def __init__(self):
        self.graph = defaultdict(WeightedGraphNode)
        self.graph_node_item_constructor = namedtuple("Vertex", ["key", "weight", "vertex"])
        self.table_of_shortest_paths = dict()
        self.minimum_spanning_tree = []
        self.visited_check = set()

    def add_edge(self, from_vertex: int, to_vertex: int, weigth: int) -> None:
        """
        Добавление ребра в граф
        """
        getattr(self.graph[from_vertex], 'adjacent_vertices').append(self.graph_node_item_constructor(to_vertex, weigth, self.graph[from_vertex]))
        getattr(self.graph[to_vertex], 'adjacent_vertices').append(self.graph_node_item_constructor(from_vertex, weigth, self.graph[to_vertex]))
        self.table_of_shortest_paths[from_vertex] = TableOfShortestPathsItem(weight=float("inf"), vertex=self.graph[from_vertex], key=from_vertex)
        self.table_of_shortest_paths[to_vertex] = TableOfShortestPathsItem(weight=float("inf"), vertex=self.graph[to_vertex], key=to_vertex)

    def prim_algorithm(self) -> List[int]:
        """
        Находим минимальное остовное дерево методом Прима
        """
        _, vertex = choice(list(self.table_of_shortest_paths.items()))

        stack = []

        stack.append(vertex)
        del self.table_of_shortest_paths[vertex.key]

        while stack:
            vertex = stack.pop()
            self.visited_check.add(vertex.key)
            self.minimum_spanning_tree.append(vertex.key)

            for _key, weight, _vertex in vertex.vertex.adjacent_vertices:
                if _key not in self.visited_check:
                    __vertex = self.table_of_shortest_paths[_key]
                    if __vertex.weight > weight:
                        __vertex.weight = weight

            if self.table_of_shortest_paths:
                min_vertex = min(self.table_of_shortest_paths.values(), key=lambda vertex: vertex.weight)
                del self.table_of_shortest_paths[min_vertex.key]
                stack.append(min_vertex)
        return self.minimum_spanning_tree


g = WeightedGraph()

g.add_edge(0, 3, 10)
g.add_edge(0, 8, 3)
g.add_edge(0, 1, 9)

g.add_edge(8, 3, 11)
g.add_edge(8, 1, 16)

g.add_edge(1, 4, 8)
g.add_edge(1, 2, 4)

g.add_edge(2, 4, 14)
g.add_edge(2, 5, 1)

g.add_edge(3, 4, 7)
g.add_edge(3, 6, 13)
g.add_edge(3, 7, 5)

g.add_edge(4, 5, 12)
g.add_edge(4, 6, 15)

g.add_edge(6, 5, 2)
g.add_edge(6, 7, 6)
