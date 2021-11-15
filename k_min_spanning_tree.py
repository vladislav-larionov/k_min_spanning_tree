import sys

from graph import Graph, Node
from graph_obj_reader import read_graph_as_obj_from_matrix
from print_utils import print_result1, print_result_to_file


def find_mins(graph):
    indies = set()
    min = 1000000000000000
    for i in range(len(graph.adj_mat)):
        if graph.adj_mat[i][0] != 0:
            min = graph.adj_mat[i][0]
            break
    for i in range(len(graph.adj_mat)):
        for j in range(len(graph.adj_mat)):
            if graph.adj_mat[i][j] != 0 and graph.adj_mat[i][j] < min:
                min = graph.adj_mat[i][j]
                indies.clear()
                indies.add(graph.node(i))
            elif graph.adj_mat[i][j] != 0 and graph.adj_mat[i][j] == min:
                indies.add(graph.node(i))
    return indies


def nodes_to_str(nodes):
    sorted_n = map(lambda n1:str(n1.index), sorted(nodes, key=lambda n:n.index))
    return '_'.join(sorted_n)


def find_k_min_spanning_tree(graph, k):
    solution = get_first_spanning_tree(graph, k)
    tree_nodes, tree_edges, res_tree_nodes, res_tree_edges = set(), set(), set(), set()
    print(solution.graph_weight())
    mins = graph.nodes
    results = set()
    for start in mins:
        s_pos = start
        res, tree_nodes, tree_edges = find_spanning_tree(graph, s_pos, k)
        nodes_as_str = nodes_to_str(tree_nodes)
        if nodes_as_str in results:
            continue
        results.add(nodes_as_str)
        print_result_to_file(k, res, graph, tree_edges)
        graph_weight = res.graph_weight()
        if graph_weight < solution.graph_weight():
            res_tree_nodes, res_tree_edges, solution = tree_nodes, tree_edges, res
    print()
    print(solution.graph_weight())
    return solution, res_tree_nodes, res_tree_edges


def get_middle_nodes(graph, k):
    middle = int(len(graph.nodes)/2)
    indies = range(middle - 4*k, middle + 4*k)
    nodes = [graph.node(i) for i in indies]
    mid = int(len(indies)/2)
    return nodes[mid:] + nodes[:mid]


def find_spanning_tree(graph, start_node, k):
    tree_edges = set()
    tree_nodes = {start_node}
    middle = int(len(graph.nodes)/2)
    while len(tree_edges) < k - 1:
        nearest_edges = find_min_nearest_node(graph, tree_nodes)
        nearest_edge = None
        if len(nearest_edges) > 1:
            nearest_edge = sorted(nearest_edges, key=lambda e:e[1].index)[int(len(nearest_edges) / 2)]
        else:
            nearest_edge = nearest_edges.pop()
        tree_edges.add((nearest_edge[0], nearest_edge[1], nearest_edge[2]))
        tree_nodes.add(nearest_edge[1])
    tree = Graph.create_from_nodes([Node(data=node.data) for node in tree_nodes])
    for edge in tree_edges:
        tree.connect(tree.node_by_value(edge[0].data), tree.node_by_value(edge[1].data), edge[2], False)
    return tree, tree_nodes, tree_edges


def find_min_nearest_node(graph, tree_nodes) -> set:
    cands = dict()
    for node in tree_nodes:
        nodes = list(filter(lambda n: n[0] not in tree_nodes, graph.connections_from(node)))
        for adj_node in nodes:
            cands[adj_node[1]] = cands.get(adj_node[1], list())
            cands[adj_node[1]].append((node, adj_node[0], adj_node[1]))
    return cands[sorted(cands.keys())[0]]


def get_first_spanning_tree(graph, k):
    nodes = graph.nodes[:k]
    tree = Graph.create_from_nodes(nodes)
    for i in range(k-1):
        tree.connect(nodes[i], nodes[i + 1], graph.get_weight(nodes[i], nodes[i + 1]), False)
    return tree


def main():
    benchmark_file_path = sys.argv[1]
    graph = read_graph_as_obj_from_matrix(benchmark_file_path)
    k_min_spanning_tree, tree_nodes, tree_edges = find_k_min_spanning_tree(graph, int(len(graph.nodes) / 8))
    print_result1(k_min_spanning_tree, graph, tree_nodes, tree_edges)

if __name__ == '__main__':
    main()
