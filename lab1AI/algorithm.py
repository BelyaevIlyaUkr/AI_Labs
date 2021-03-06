import random
import math


class Graph:
    def __init__(self, connection_matrix, number_of_nodes, number_of_edges, chromatic_number):
        self.__connection_matrix = connection_matrix
        self.__number_of_nodes = number_of_nodes
        self.__number_of_edges = number_of_edges
        self.__chromatic_number = chromatic_number
        self.__colors_of_nodes = []

        self.__fill_graph_with_random_colors()

    def __fill_graph_with_random_colors(self):
        for i in range(len(self.__number_of_nodes)):
            self.__colors_of_nodes.append(random.randint(0, self.__chromatic_number - 1))

    def coloring_without_conflicts(self, number_of_ants):
        pc = 0.5
        ants_positions = [0 for i in range(number_of_ants)]
        iteration_number = 1
        while self.__confsoverall() != 0:
            chosen_node = 0
            
            for i in range(number_of_ants):
                probability_for_node = random.random()

                if probability_for_node <= self.__pn(self.__maxconf(), self.__confsoverall(), iteration_number):
                    chosen_node = self.__find_the_worst_neighbour_node(ants_positions[i])
                else:
                    chosen_node = random.randint(0, self.__number_of_nodes - 1)
                ants_positions[i] = chosen_node

                probability_for_color = random.random()
                if probability_for_color <= pc:
                    self.__try_paint_node_with_the_best_color(chosen_node)
                else:
                    self.__colors_of_nodes[chosen_node] = \
                        random.randint(0, self.__chromatic_number - 1)

            iteration_number += 1

    def __pn(self, maxconf, confsoverall, iteration_number):
        avgy = 4.8 * confsoverall / (self.__number_of_nodes)
        avgx = 1 * maxconf
        return math.exp(-3.2 * ((5 * iteration_number + 1) * avgy / (avgx)))

    def __maxconf(self):
        max_conflict = 0

        for node_number in range(self.__number_of_nodes):
            number_of_conflict_in_node = self.__calculate_number_of_conflicts_in_node(node_number)
            if max_conflict < number_of_conflict_in_node:
                max_conflict = number_of_conflict_in_node

        return max_conflict

    def __calculate_number_of_conflicts_in_node(self, consideration_node_number):
        number_of_conflicts = 0

        for node_number in range(self.__number_of_nodes):
            if (node_number != consideration_node_number and
            self.__connection_matrix[consideration_node_number][node_number] == 1 and
            self.__colors_of_nodes[consideration_node_number] == self.__colors_of_nodes[node_number]):
                number_of_conflicts += 1

        return number_of_conflicts

    def __confsoverall(self):
        conflictsoverall = 0

        for node_number in range(self.__number_of_nodes):
            conflictsoverall += self.__calculate_number_of_conflicts_in_node(node_number)

        return conflictsoverall

    def __find_the_worst_neighbour_node(self, current_node):
        max_neighbour_conf = 0
        the_worst_neighbour_conf = 0

        for node in range(self.__number_of_nodes):
            if current_node != node and self.__connection_matrix[current_node][node] == 1:
                number_of_conflicts_in_node = self.__calculate_number_of_conflicts_in_node(node)
                if number_of_conflicts_in_node > max_neighbour_conf:
                    max_neighbour_conf = number_of_conflicts_in_node
                    the_worst_neighbour_conf = node

        return the_worst_neighbour_conf

    def __try_paint_node_with_the_best_color(self, current_node):
        min_number_of_conflicts = self.__calculate_number_of_conflicts_in_node(current_node)
        primary_min_number_of_conflicts = min_number_of_conflicts

        for color in range(self.__chromatic_number):
            self.__colors_of_nodes[current_node] = color
            number_of_conflicts = self.__calculate_number_of_conflicts_in_node(current_node)
            if number_of_conflicts < min_number_of_conflicts:
                min_number_of_conflicts = number_of_conflicts
                break

        if min_number_of_conflicts == primary_min_number_of_conflicts:
            best_number_of_conflicts = 1000000
            for color in range(self.__chromatic_number):
                previous_color = self.__colors_of_nodes[current_node]
                self.__colors_of_nodes[current_node] = color
                number_of_conflicts = self.__calculate_number_of_conflicts_in_node(current_node)
                if number_of_conflicts < best_number_of_conflicts:
                    best_number_of_conflicts = number_of_conflicts
                else:
                    self.__colors_of_nodes[current_node] = previous_color
