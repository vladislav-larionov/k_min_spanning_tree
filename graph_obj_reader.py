from graph import Node, Graph
from graph_reader import compute_distance, read_vertexes


def create_graph(vertexes_):
    graph = Graph.create_from_nodes([Node(str(i + 1)) for i, vertex in enumerate(vertexes_)])
    for i in range(len(graph.nodes)):
        for j in range(len(graph.nodes)):
            if i != j:
                graph.connect(graph.nodes[i], graph.nodes[j], compute_distance(vertexes_[i], vertexes_[j]))
    return graph


def read_graph_as_obj(filename):
    vertexes_ = read_vertexes(filename)
    return create_graph(vertexes_)


def read_matrix(filename):
    with open(filename) as file:
        return list(map(lambda l: [int(v) for v in l.split(', ')], file.readlines()))


def read_graph_as_obj_from_matrix(filename):
    matrix = read_matrix(filename)
    return create_graph_from_matrix(matrix)


def create_graph_from_matrix(matrix):
    graph = Graph.create_from_nodes([Node(str(i + 1)) for i, vertex in enumerate(matrix)])
    for i in range(len(graph.nodes)):
        for j in range(len(graph.nodes)):
            if i != j:
                graph.connect(graph.nodes[i], graph.nodes[j], matrix[i][j])
    return graph


if __name__ == '__main__':
    # vertexes = read_vertexes('Benchmark/Taxicab_64.txt')
    # vertexes = create_graph(vertexes)
    graph = read_graph_as_obj_from_matrix('Taxicab_64_matrix.txt')
    graph.print_adj_mat()
    for node in graph.nodes:
        print(f"{node}: {graph.connections_from(node)}")

