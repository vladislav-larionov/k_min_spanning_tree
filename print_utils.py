from graph import Graph


def print_matrix(matrix):
    for row in matrix:
        print(", ".join(map(str, row)))


def print_result(k_min_spanning_tree: Graph, orig_graph: Graph):
    print(f'c Вес дерева = {k_min_spanning_tree.graph_weight()}, число листьев = {k_min_spanning_tree.leaf_count()}')
    edges = list()
    for node in k_min_spanning_tree.nodes:
        for connected in set(map(lambda c: c[0].data, k_min_spanning_tree.connections_from(node))):
            edges.append(f"e {node.data} {connected}")
    print(f'p edge {len(orig_graph.nodes)} {len(edges)}')
    for edge in edges:
        print(edge)


def print_result1(k_min_spanning_tree: Graph, orig_graph: Graph, tree_nodes, tree_edges):
    print(f'c Вес дерева = {sum(map(lambda e: e[2],tree_edges))}, число листьев = {k_min_spanning_tree.leaf_count(tree_edges)}')
    print(f'p edge {len(orig_graph.nodes)} {len(tree_edges)}')
    # for e in sorted([f"e {edge[0].data} {edge[1].data} {edge[2]}\n" for edge in tree_edges]):
    for e in sorted([f"e {edge_to_str(edge)}\n" for edge in tree_edges]):
        print(e, end='')


def print_result_to_file(k, k_min_spanning_tree: Graph, orig_graph: Graph, tree_edges):
    with open(f'temp_res_{k}.txt', 'a+', encoding='utf-8') as file:
        file.write(f'c Вес дерева = {sum(map(lambda e: e[2],tree_edges))}, число листьев = {k_min_spanning_tree.leaf_count(tree_edges)}\n')
        file.write(f'p edge {len(orig_graph.nodes)} {len(tree_edges)}\n')
        for e in sorted([f"e {edge_to_str(edge)}\n" for edge in tree_edges]):
            file.write(e)
        file.write("\n")
        # for edge in tree_edges:
        #     file.write(f"{edge}\n")
        # for row in k_min_spanning_tree.adj_mat:
        #     file.write(f'{", ".join(map(str, row))}\n')
        # file.write("\n")
        file.write("-------------------------------------------")
        file.write("\n")


def edge_to_str(edge):
    if int(edge[0].data) < int(edge[1].data):
        return edge[0].data + " " + edge[1].data
    else:
        return edge[1].data + " " + edge[0].data

def print_matrix_graph(matrix):
    print('   |\t', end='')
    for i, _ in enumerate(matrix):
        print(f'{i+1:3}\t', end='')
    print()
    for j, row in enumerate(matrix):
        print(f'{j+1:3}|\t' + "\t".join([f'{el:3}' for el in row]))
