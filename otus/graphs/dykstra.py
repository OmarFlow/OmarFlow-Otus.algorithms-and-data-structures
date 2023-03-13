from collections import defaultdict
from typing import Optional, Dict


class WeightedGraphNode:
    """
    Вершина/нода графа
    """
    def __init__(self):
        self.key: Optional[str] = None
        self.weight: Optional[int] = None
        self.adjacent_vertices = []


class AdjacentVertex:
    """
    Смежная вершина
    """
    def __init__(self, key: str, value: WeightedGraphNode, weight: int):
        self.key = key
        self.weight = weight
        self.value = value
        self.pool = []


class WeightedGraph:
    """
    Взвешенный граф
    """
    def __init__(self):
        self.graph = defaultdict(WeightedGraphNode)
        self.sorted_vertices = []

    def add_edge(self, from_vertex_key: str, to_vertex_key: str, weigth: int) -> None:
        """
        Добавление ребра в граф
        """
        from_vertex = self.graph[from_vertex_key]
        from_vertex.key = from_vertex_key
        to_vertex = self.graph[to_vertex_key]
        to_vertex.key = to_vertex_key
        getattr(from_vertex, 'adjacent_vertices').append(AdjacentVertex(key=to_vertex.key, value=to_vertex, weight=weigth))
        getattr(to_vertex, 'adjacent_vertices').append(AdjacentVertex(key=from_vertex.key, value=from_vertex, weight=weigth))

    def descending_insert(self, vert: WeightedGraphNode, left_item_index=1, right_item_index=2) -> None:
        """
        Вставляет элементы в массив по порядку убывания
        """
        num = vert.weight
        if not self.sorted_vertices:
            self.sorted_vertices.append(vert)
            return

        if len(self.sorted_vertices) == 1:
            if num >= self.sorted_vertices[0].weight:
                self.sorted_vertices.insert(0, vert)
            else:
                self.sorted_vertices.append(vert)
            return

        if self.sorted_vertices[0].weight <= num:
            self.sorted_vertices.insert(0, vert)
            return

        if num <= self.sorted_vertices[1].weight:
            if len(self.sorted_vertices) == 2:
                self.sorted_vertices.append(vert)
                return

        try:
            if num < self.sorted_vertices[left_item_index].weight and num > self.sorted_vertices[
                right_item_index].weight:
                self.sorted_vertices.insert(right_item_index, vert)
                return
            elif num > self.sorted_vertices[left_item_index].weight:
                self.sorted_vertices.insert(left_item_index, vert)
            else:
                self.descending_insert(vert, left_item_index + 1, right_item_index + 1)
        except IndexError:
            self.sorted_vertices.append(vert)
            return

    def dykstra(self, key: str) -> Dict[str, int]:
        """
        Нахождение кратчайшего пути от заданной вершины к другим методом Дейкстры
        """
        vertex = self.graph[key]
        shortest_path_map = {}

        #смотрим длину пути смежных вершин
        for adj_vert in vertex.adjacent_vertices:
            vert = adj_vert.value
            vert.weight =adj_vert.weight
            self.descending_insert(vert)
        shortest_path_map[vertex.key] = 0

        while self.sorted_vertices:
            #выбираем вершину с кротчайшим путём
            min_weight_vert = self.sorted_vertices.pop()

            #записываем этот путь
            shortest_path_map[min_weight_vert.key] = min_weight_vert.weight

            #проходимся по смежным вершинам и рассчитываем пути
            for adj_vert in min_weight_vert.adjacent_vertices:
                vert = adj_vert.value
                if vert.key in shortest_path_map.keys():
                    continue
                # если путь в обход короче - записываем его
                if vert in self.sorted_vertices:
                    if min_weight_vert.weight + adj_vert.weight < vert.weight:
                        vert.weight = min_weight_vert.weight + adj_vert.weight
                    continue
                vert.weight = adj_vert.weight + min_weight_vert.weight
                self.descending_insert(vert)
        return shortest_path_map


# g = WeightedGraph()
#
# g.add_edge('g', 'e', 5)
# g.add_edge('g', 'f', 8)
#
# g.add_edge('e', 'f', 1)
# g.add_edge('e', 'c', 7)
# g.add_edge('e', 'b', 9)
#
# g.add_edge('f', 'c', 6)
# g.add_edge('f', 'd', 4)
#
# g.add_edge('c', 'b', 4)
# g.add_edge('c', 'a', 3)
# g.add_edge('c', 'd', 1)
#
# g.add_edge('a', 'b', 2)
# g.add_edge('a', 'd', 6)
