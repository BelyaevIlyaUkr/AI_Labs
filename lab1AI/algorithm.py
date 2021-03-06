import random
import math


# функція зчитування вхідного файлу
def scan_input_file(filename):
    split_filename = filename.split('.')
    chromatic_number = int(split_filename[1])
    number_of_nodes = 0
    number_of_edges = 0
    connection_matrix = []

    f = open("yuzGCP130.13.col", "r")

    for line in f:
        split_line = line.split(" ")
        if split_line[0] == "p":
            number_of_nodes = int(split_line[2])
            number_of_edges = int(split_line[3])
            connection_matrix = [[0 for i in range(number_of_nodes)] for j in range(number_of_nodes)]
        elif split_line[0] == "e":
            connection_matrix[int(split_line[1]) - 1][int(split_line[2]) - 1] = 1
            connection_matrix[int(split_line[2]) - 1][int(split_line[1]) - 1] = 1

    return connection_matrix, number_of_nodes, number_of_edges, chromatic_number


# клас для роботи з графом
class Graph:
    # конструктор класу
    def __init__(self, connection_matrix, number_of_nodes, number_of_edges, chromatic_number):
        # матриця з'єднань графу
        self.__connection_matrix = connection_matrix
        # кількість вершин в графі
        self.__number_of_nodes = number_of_nodes
        # кількість ребер в графі
        self.__number_of_edges = number_of_edges
        # хроматичне число
        self.__chromatic_number = chromatic_number
        # кольори вершин графу
        self.__colors_of_nodes = []

        self.__fill_graph_with_random_colors()

    # функція початкової розкраски графу випадковими кольорами згідно з хроматичним числом
    def __fill_graph_with_random_colors(self):
        for i in range(self.__number_of_nodes):
            self.__colors_of_nodes.append(random.randint(0, self.__chromatic_number - 1))

    # функція безконфліктної розкраски графу
    def coloring_without_conflicts(self, number_of_ants):
        pc = 0.9
        ants_positions = [0 for i in range(number_of_ants)]
        iteration_number = 0
        while self.__confsoverall() != 0:
            chosen_node = 0
            print(self.__confsoverall())
            for i in range(number_of_ants):
                probability_for_node = random.random()

                if probability_for_node <= self.__pn(i+1, i+1, i+1):
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

    # функція рахування ймовірності Pn (ймовірність вибору найгіршого сусіда)
    def __pn(self, maxconf, confsoverall, iteration_number):
        avgy = 4.8 * confsoverall / (self.__number_of_nodes)
        avgx = 1 * maxconf
        return math.exp(-3.2 * ((5 * iteration_number + 1) * avgy / (avgx)))

    # функція знаходження максимального конфлікту в графі
    def __maxconf(self):
        max_conflict = 0

        for node_number in range(self.__number_of_nodes):
            number_of_conflict_in_node = self.__calculate_number_of_conflicts_in_node(node_number)
            if max_conflict < number_of_conflict_in_node:
                max_conflict = number_of_conflict_in_node

        return max_conflict

    # функція знаходження кількості конфліктів певної вершини графу
    def __calculate_number_of_conflicts_in_node(self, consideration_node_number):
        number_of_conflicts = 0

        for node_number in range(self.__number_of_nodes):
            if (node_number != consideration_node_number and
            self.__connection_matrix[consideration_node_number][node_number] == 1 and
            self.__colors_of_nodes[consideration_node_number] == self.__colors_of_nodes[node_number]):
                number_of_conflicts += 1

        return number_of_conflicts

    # функція знаходження загальної кількості конфліктів в графі
    def __confsoverall(self):
        conflictsoverall = 0

        for node_number in range(self.__number_of_nodes):
            conflictsoverall += self.__calculate_number_of_conflicts_in_node(node_number)

        return conflictsoverall

    # функція знаходження сусіда з найбільшою кількістю конфліктів
    def __find_the_worst_neighbour_node(self, current_node):
        max_neighbour_conf = 0
        the_worst_neighbour_node = 0

        for node in range(self.__number_of_nodes):
            if current_node != node and self.__connection_matrix[current_node][node] == 1:
                number_of_conflicts_in_node = self.__calculate_number_of_conflicts_in_node(node)
                if number_of_conflicts_in_node > max_neighbour_conf:
                    max_neighbour_conf = number_of_conflicts_in_node
                    the_worst_neighbour_node = node

        return the_worst_neighbour_node

    # функція спроби перекраски вершини в найкращий колір (або виштовхнути з локального мінімуму)
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

    # функція виведення на екран сусідів кожної вершини
    def print_graph_connections(self):
        for i in range(self.__number_of_nodes):
            print(f"Node {i + 1}, way to ", end="")
            for j in range(self.__number_of_nodes):
                if self.__connection_matrix[i][j] == 1:
                    print(f"{j + 1}, ",end="")
            print("")

    # функція виведення на екран кольору кожної вершини
    def print_node_colors(self):
        for i in range(self.__number_of_nodes):
            print(f"Node {i + 1} - Color {self.__colors_of_nodes[i]}")


