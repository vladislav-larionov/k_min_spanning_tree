# https://python-scripts.com/dijkstras-algorithm

class Node:
    def __init__(self, data, indexloc=None):
        self.data = data
        self.index = indexloc

    def copy(self):
        return Node(self.data, self.index)

    def __repr__(self):
        return f'{self.index}("{self.data}")'
        # return f'{self.index}'


class Graph:
    @classmethod
    def create_from_nodes(cls, nodes):
        return Graph(len(nodes), len(nodes), nodes)

    def __init__(self, row, col, nodes=None):
        # установка матрица смежности
        self.adj_mat = [[0] * col for _ in range(row)]
        self.nodes = nodes
        for i in range(len(self.nodes)):
            self.nodes[i].index = i

    # Связывает node1 с node2
    # Обратите внимание, что ряд - источник, а столбец - назначение
    # Обновлен для поддержки взвешенных ребер (поддержка алгоритма Дейкстры)
    def _connect_dir(self, node1, node2, weight=1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = weight

    # Опциональный весовой аргумент для поддержки алгоритма Дейкстры
    def connect(self, node1, node2, weight=1, sim=True):
        self._connect_dir(node1, node2, weight)
        if sim:
            self._connect_dir(node2, node1, weight)

    # Получает ряд узла, отметить ненулевые объекты с их узлами в массиве self.nodes
    # Выбирает любые ненулевые элементы, оставляя массив узлов
    # которые являются connections_to (для ориентированного графа)
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_from(self, node):
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if
                self.adj_mat[node][col_num] != 0]

    # Проводит матрицу к столбцу узлов
    # Проводит любые ненулевые элементы узлу данного индекса ряда
    # Выбирает только ненулевые элементы
    # Обратите внимание, что для неориентированного графа
    # используется connections_to ИЛИ connections_from
    # Возвращает значение: массив кортежей (узел, вес)
    def connections_to(self, node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]
        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]

    def print_adj_mat(self):
        for row in self.adj_mat:
            print(', '.join(map(str, row)))

    def print_adj_mat_to_file(self, k):
        with open(f'res_{k}.txt', 'w') as file:
            for row in self.adj_mat:
                file.write(', '.join(map(str, row)) + '\n')

    def node(self, index):
        return self.nodes[index]

    def node_by_value(self, value):
        for node in self.nodes:
            if node.data == value:
                return node
        return None

    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)

    # Убирает связь в направленной манере (nod1 к node2)
    # Может принять номер индекса ИЛИ объект узла
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = 0

        # Может пройти от node1 к node2

    def can_traverse_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != 0

    def has_conn(self, node1, node2):
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)

    def add_node(self, node):
        self.nodes.append(node)
        node.index = len(self.nodes) - 1
        for row in self.adj_mat:
            row.append(0)
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))

    # Получает вес, представленный перемещением от n1
    # к n2. Принимает номера индексов ИЛИ объекты узлов
    def get_weight(self, n1, n2):
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2]

    # Разрешает проводить узлы ИЛИ индексы узлов
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    def print_connected_nodes(self):
        for node in self.nodes:
            if self.connections_from(node):
                print(f"{node}: {self.connections_from(node)}")

    def print_nodes_with_connections(self):
        for node in self.nodes:
            print(f"{node}: {self.connections_from(node)}")

    def graph_weight(self):
        weight = 0
        for i in self.adj_mat:
            weight += sum(i)
        return int(weight)

    def sum_nodes(self, node, seen, sum):
        for sub_nodes in self.connections_from(node):
            if sub_nodes[0] not in seen:
                seen.add(sub_nodes[0])
                sum = self.sum_nodes(sub_nodes[0], seen, sum + sub_nodes[1])
        return sum

    @staticmethod
    def leaf_count(edges):
        counters = dict()
        for edge in edges:
            counters[edge[0]] = counters.get(edge[0], 0)
            counters[edge[0]] += 1
            counters[edge[1]] = counters.get(edge[1], 0)
            counters[edge[1]] += 1
        leaves = sum(filter(lambda n: n == 1, counters.values()))
        return leaves

    # def leaf_count(self):
    #     leaves = 0
    #     for node in self.nodes:
    #         for connected in set(map(lambda c: c[0].data, self.connections_from(node))):
    #             if not self.connections_from(int(connected)-1):
    #                 leaves += 1
    #     return leaves

# a = Node("A")
# b = Node("B")
# c = Node("C")
# d = Node("D")
# e = Node("E")
# f = Node("F")
#
# graph = Graph.create_from_nodes([a, b, c, d, e, f])
#
# graph.connect(a, b)
# graph.connect(a, c)
# graph.connect(a, e)
# graph.connect(b, c, 5)
# graph.connect(b, d)
# graph.connect(c, d)
# graph.connect(c, f)
# graph.connect(d, e)
#
# graph.print_adj_mat()
#
# for node in graph.nodes:
#     print(f"{node}: {graph.connections_from(node)}")
