import algorithm

if __name__ == '__main__':
    connection_matrix, number_of_nodes, number_of_edges, chromatic_numbers = \
        algorithm.scan_input_file("yuzGCP130.13.col")

    graph = algorithm.Graph(connection_matrix, number_of_nodes, number_of_edges, chromatic_numbers)

    graph.coloring_without_conflicts(4)

    graph.print_graph_connections()

    graph.print_node_colors()


