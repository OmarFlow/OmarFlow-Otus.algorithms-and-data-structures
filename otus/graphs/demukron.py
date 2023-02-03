from copy import copy
from typing import List, Tuple
from collections import defaultdict


class OrGraphNode:
    def __init__(self):
        self.incoming = []
        self.outgoing = []

    @property
    def half_incoming_degree(self) -> int:
        """""
        Полустепень входа
        """""
        return len(self.incoming)


class OrGraph:
    def __init__(self):
        self.graph = defaultdict(OrGraphNode)
        self.root = self.graph[0]

    def add_edge(self, from_vertex: int, to_vertex: int, direction: str) -> None:
        """
        Добавление ребра в граф
        """
        another_direction = "incoming" if direction == "outgoing" else "outgoing"
        getattr(self.graph[from_vertex], direction).append(to_vertex)
        getattr(self.graph[to_vertex], another_direction).append(from_vertex)

    def demukron_sorting(self) -> List[Tuple[int, OrGraphNode]]:
        """
        Топологическая сортировка демукрона
        """
        graph = copy(self.graph)
        res = []
        work = []

        while any(i.half_incoming_degree != 0 for i in copy(graph).values()):
            for key, value in copy(graph).items():
                if value.half_incoming_degree == 0:
                    work.extend(value.outgoing)
                    res.append((key, value))
                    del graph[key]

            for key in work:
                graph[key].incoming.pop()
            work.clear()

        for key, value in graph.items():
            res.append((key, value))

        return res

    # вариант более медленный, но с меньшими затратами по памяти
    # def demo(self):
    #     graph = copy(self.graph)
    #     res = []
    #     res_w = set()
    #     work = []
    #
    #     while any(i.half_incoming_degree != 0 for i in graph.values()):
    #         for key, value in graph.items():
    #             if value.half_incoming_degree == 0 and value not in res_w:
    #                 work.extend(value.outgoing)
    #                 res.append((key, value))
    #                 res_w.add(value)
    #
    #         for key in work:
    #             graph[key].incoming.pop()
    #         work.clear()
    #
    #     for key, value in graph.items():
    #         if value.half_incoming_degree == 0 and value not in res_w:
    #             res.append((key, value))
    #
    #     return res


# g = OrGraph()
# g.add_edge(0, 1, "outgoing")
#
# g.add_edge(1, 2, "outgoing")
# g.add_edge(1, 4, "outgoing")
# g.add_edge(1, 6, "outgoing")
# g.add_edge(1, 3, "outgoing")
#
# g.add_edge(2, 4, "outgoing")
#
# g.add_edge(3, 5, "outgoing")
# g.add_edge(3, 6, "outgoing")
#
# g.add_edge(4, 6, "outgoing")
#
# g.add_edge(6, 7, "outgoing")
#
# g.add_edge(7, 5, "outgoing")
