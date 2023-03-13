class OrGraphEdge:
    """
    Ребро графа
    """
    def __init__(self, _from, _to, _cost):
        self._from: str = _from
        self._to: str = _to
        self.key: str = _from + _to
        self._cost: int = _cost

    def __str__(self):
        return self.key


class OrGraph:
    """
    Ориентированно-взвешенный граф
    """
    def __init__(self):
        self.edges = []
        self.vertexes = set()

    def add_edge(self, from_vertex: str, to_vertex: str, cost: int) -> None:
        """
        Добавление ребра в граф
        """
        self.edges.append(OrGraphEdge(from_vertex, to_vertex, cost))
        self.vertexes.add(from_vertex)
        self.vertexes.add(to_vertex)

    def bellman_ford(self, vertex: str):
        """
        Нахождение кратчайшего пути от заданной вершины к другим методом Беллмана - Форда
        """
        vertex_to_vertex_cost_map = {vertex+_vertex: float("inf") for _vertex in self.vertexes if vertex != _vertex}
        for _ in range(len(self.vertexes) - 1):
            for edge in self.edges:
                # исключаем путь до себя
                if edge._to == vertex:
                    continue
                # если инцедентые ребра не заполнены - заполняем
                if vertex == edge._from and vertex_to_vertex_cost_map[edge.key] == float('inf'):
                    vertex_to_vertex_cost_map[edge.key] = edge._cost
                    continue
                # опять же исключаем путь до себя
                elif vertex == edge._from and vertex_to_vertex_cost_map[edge.key] != float('inf'):
                    continue
                # если путь в обход дешевле - записываем
                if vertex_to_vertex_cost_map[vertex + edge._to] > vertex_to_vertex_cost_map[vertex + edge._from] + edge._cost:
                    vertex_to_vertex_cost_map[vertex + edge._to] = vertex_to_vertex_cost_map[vertex + edge._from] + edge._cost

        return vertex_to_vertex_cost_map

# g = OrGraph()
#
# g.add_edge('1', '2', -2)
# g.add_edge('1', '3', 5)
# g.add_edge('1', '4', 7)
#
# g.add_edge('2', '3', 6)
# g.add_edge('2', '4', 8)
#
# g.add_edge('3', '1', -1)
#
# g.add_edge('4', '2', 3)
# g.add_edge('4', '3', -4)
