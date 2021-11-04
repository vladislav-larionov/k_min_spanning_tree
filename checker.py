import sys
from pprint import pprint

from graph import Graph
from graph_obj_reader import read_graph_as_obj_from_matrix


def read_res(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        weight = int(file.readline().split(', ')[0].split(' ')[-1])
        n = int(file.readline().split(' ')[-1])
        print(f'w = {weight} n = {n}')
        edges = [list(map(int, line.lstrip('e ').split(' '))) for line in file.readlines()[:n]]
        # for row in edges:
        #     print(row)
    return edges, weight


def check_edge_existing(graph, edges, weight):
    total_weight = 0
    for edge in edges:
        total_weight += graph.adj_mat[edge[0] - 1][edge[1] - 1]
    return total_weight == weight


def main():
    res_file_path = sys.argv[1]
    benchmark_file_path = sys.argv[2]
    graph = read_graph_as_obj_from_matrix(benchmark_file_path)
    edges, weight = read_res(res_file_path)
    print(check_edge_existing(graph, edges, weight))


if __name__ == '__main__':
    main()