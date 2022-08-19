class Vertex:
    """Представление вершины графа"""
    def __init__(self, name=""):
        self._links = []
        self.name = name

    @property
    def links(self):
        return self._links

    def __hash__(self):
        return hash(self.name)

class Link:
    """Описание связи между двумя произвольными вершинами графа"""
    def __init__(self, v1, v2, dist=1):
        self._v1 = v1
        self._v2 = v2
        self._dist = dist  # может быть любым значением с любым свойством (км, мин и т.п)

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist
    @dist.setter
    def dist(self, value):
        if value < 0:
            raise AttributeError("Link weight must be positive number")
        self._dist = value

    # проверка однозначности маршрутов (v1 -> v2 == v2 -> v1, а значит новый маршрут добавлять не нужно)
    def __eq__(self, other):
        if type(other) not in (Link, LinkMetro):
            raise TypeError("type object must be 'Link'")
        return self.v1 == other.v1 and self.v2 == other.v2 or self.v1 == other.v2 and self.v2 == other.v1

class LinkedGraph:
    """Описание всего графа"""
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if type(v) not in (Vertex, Station):
            raise TypeError("variable type have to be Vertex")
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if type(link) not in (Link, LinkMetro):
            raise TypeError("variable type have to be Link")
        if link not in self._links:
            self._links.append(link)
            """В случае добавления пути с вершинами, которых нет в списке vertex, их нужно тоже добавить"""
            if link.v1 not in self._vertex:
                self._vertex.append(link.v1)
            if link.v2 not in self._vertex:
                self._vertex.append(link.v2)

    # данный метод реализуется при помощи алгоритма Дейкстры
    def find_path(self, start_v, stop_v):
        """возвращает кратчайший маршрут в виде ([вершины], [связи])"""

        def find_lowest_node(costs):
            """нахождение минимального расстояния"""
            lowest_cost = float("inf")
            lowest_cost_node = None
            for node in costs:
                cost = costs[node]
                if cost < lowest_cost and node not in processed:
                    lowest_cost = cost
                    lowest_cost_node = node
            return lowest_cost_node

        #------ подготовка данных
        matrix = self.init_adj_matrix()
        graph, costs, parents = self.init_data(matrix, start_v)


        #------ сам алгоритм
        processed = []
        node = find_lowest_node(costs)
        while node is not None:
            cost = costs[node]
            neighbours = graph[node]
            for n in neighbours.keys():
                if n is not start_v:
                    new_cost = cost + neighbours[n]
                    if costs[n] > new_cost:
                        costs[n] = new_cost
                        parents[n] = node
            processed.append(node)
            node = find_lowest_node(costs)


        # составляем ответ
        res_vertexes = []
        res_links = []

        tmp = stop_v
        while tmp is not start_v:
            res_vertexes.append(tmp)
            for link in self._links:
                if link.v1 is tmp and link.v2 is parents[tmp] or link.v2 is tmp and link.v1 is parents[tmp]:
                    res_links.append(link)
                    break
            tmp = parents[tmp]
        res_vertexes.append(start_v)

        return res_vertexes[::-1], res_links[::-1]


    def init_data(self, matrix, start_v):
        """подготовка данных из матрицы смежности"""

        graph = {}
        costs = {}
        parents = {}

        processed = []
        for link in self._links:
            if link.v1 is start_v:
                costs[link.v2] = link.dist
                parents[link.v2] = link.v1
                processed.append(link.v2)
            elif link.v2 is start_v:
                costs[link.v1] = link.dist
                parents[link.v1] = link.v2
                processed.append(link.v1)
            else:
                if link.v1 not in processed:
                    costs[link.v1] = float("inf")
                    parents[link.v1] = float("inf")
                if link.v2 not in processed:
                    costs[link.v2] = float("inf")
                    parents[link.v2] = float("inf")

        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[i])):
                if matrix[i][j] != 0:
                    if matrix[i][0] in graph.keys():
                        graph[matrix[i][0]][matrix[0][j]] = matrix[i][j]
                    else:
                        graph[matrix[i][0]] = {matrix[0][j]: matrix[i][j]}

        return graph, costs, parents

    def init_adj_matrix(self):
        """возвращает матрицу смежности по двум спискам"""

        n = len(self._vertex)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(len(matrix)):
            matrix[i].insert(0, self._vertex[i])
        matrix.insert(0, self._vertex)
        matrix[0].insert(0, 0)
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                for link in self._links:
                    if matrix[i][0] == link.v1 and matrix[0][j] == link.v2:
                        matrix[i][j] = link.dist
                        matrix[j][i] = link.dist
        return matrix

class Station(Vertex):
    def __init(self, name):
        super().__init__(name)
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2, dist)
