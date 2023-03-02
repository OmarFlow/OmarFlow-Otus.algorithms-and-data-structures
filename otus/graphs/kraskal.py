from typing import List, Optional
from dataclasses import dataclass
from collections import defaultdict


class WeightedGraphNode:
    """
    Вершина/нода графа
    """
    def __init__(self):
        self.parent: Optional[WeightedGraphNode] = None
        self.key: Optional[int] = None
        self.link: Optional[WeightedGraphNode] = None
        self.adjacent_vertices = []

    def move_to_parent(self) -> Optional['WeightedGraphNode']:
        if self.parent == self:
            return self
        return self.link.move_to_parent()

    @property
    def has_parent(self) -> bool:
        if self.link or self.parent:
            return True
        return False

    def __str__(self):
        return str(self.key)


@dataclass
class WeightedGraphEdge:
    """
    Ребко взвешенного графа
    """
    weight: float
    vertices: List[WeightedGraphNode] = list


class WeightedGraph:
    """
    Взвешенный граф
    """
    def __init__(self):
        self.graph = defaultdict(WeightedGraphNode)
        self.edges = []
        self.minimum_spanning_tree = []
        self.parents = set()

    def add_edge(self, from_vertex_key: int, to_vertex_key: int, weigth: int) -> None:
        """
        Добавление ребра в граф
        """
        from_vertex = self.graph[from_vertex_key]
        from_vertex.key = from_vertex_key
        to_vertex = self.graph[to_vertex_key]
        to_vertex.key = to_vertex_key
        getattr(from_vertex, 'adjacent_vertices').append(to_vertex)
        getattr(to_vertex, 'adjacent_vertices').append(from_vertex)
        self.edges.append(WeightedGraphEdge(weigth, [from_vertex, to_vertex]))

    def kraskal_algorithm(self) -> List[int]:
        """
        Находим минимальное остовное дерево методом Краскала
        """
        sorted_edges = sorted(self.edges, key=lambda e: e.weight)

        for edge in sorted_edges:
            edge1 = edge.vertices[0]
            edge2 = edge.vertices[1]

            if (not edge1.has_parent) and (not edge2.has_parent):
                edge1.parent = edge1
                self.parents.add(edge1.key)
                edge2.link = edge1
                self.minimum_spanning_tree.append(edge)
                continue

            if not all(i.has_parent for i in [edge1, edge2]):
                if edge1.has_parent:
                    edge2.link = edge1
                else:
                    edge1.link = edge2
                self.minimum_spanning_tree.append(edge)
                continue

            if all(i.has_parent for i in [edge1, edge2]):
                parent1 = edge1.move_to_parent()
                parent2 = edge2.move_to_parent()
                if parent1 == parent2:
                    continue
                self.parents.remove(parent2.key)
                parent2.parent = None
                parent2.link = parent1
                edge2.link = edge1
                self.minimum_spanning_tree.append(edge)
        return self.minimum_spanning_tree


# g = WeightedGraph()
#
# g.add_edge(0, 3, 10)
# g.add_edge(0, 8, 3)
# g.add_edge(0, 1, 9)
#
# g.add_edge(8, 3, 11)
# g.add_edge(8, 1, 16)
#
# g.add_edge(1, 4, 8)
# g.add_edge(1, 2, 4)
#
# g.add_edge(2, 4, 14)
# g.add_edge(2, 5, 1)
#
# g.add_edge(3, 4, 7)
# g.add_edge(3, 6, 13)
# g.add_edge(3, 7, 5)
#
# g.add_edge(4, 5, 12)
# g.add_edge(4, 6, 15)
#
# g.add_edge(6, 5, 2)
# g.add_edge(6, 7, 6)
