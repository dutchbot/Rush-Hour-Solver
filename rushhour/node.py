from rushhour import helper


class Node:
    neighbours = []
    matrix = None
    hash_identifier = ""
    rr_moved = 0

    def __init__(self, matrix):
        self.matrix = matrix
        self.hash_identifier = helper.generate_hash(matrix)

    def update_hash(self):
        self.hash_identifier = helper.generate_hash(self.matrix)

    def get_matrix(self):
        return self.matrix

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def get_neighbours(self):
        return self.neighbours

    def has_rr_moved(self):
        return self.rr_moved > 0

    def sts(self):
        return self.__str__()

    def __str__(self):
        return str(self.hash_identifier)

    def __eq__(self, other):
        return str(self.hash_identifier) == other

    def __repr__(self):
        return str(self.hash_identifier)
