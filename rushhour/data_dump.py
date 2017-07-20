"""
    Contains the data dump class to dump rush hour steps (matrices) to a file.
"""
import os
import numpy as np
from rushhour import helper
from rushhour import constant
from rushhour.solver import solver_bfs


class DataDump:
    """
        Has methods to help with dumping all steps that a solver produces to file.
        So that you might use this data for a machine learning practice.
    """
    # negative,positive, neutral
    labels = ['neg', 'pos', 'neu']
    prefix_file = 'lvl'
    ext = 'txt'
    folder = "data"

    def dump_data_to_file(self):
        """
            For every level in given text file, we solve it and return the 'neutral' matrices.
            We then compare these with the know positive steps to take,
            so that we get negative and positive examples.
            Expect to see small positive and high negative numbers,
            and one neutral case the starting matrix.
        """
        file = open('levels.txt', 'r')
        try:
            for line in file.readlines():
                text = line.split(" ")[0]
                filename = "lvl" + line.split(" ")[1][-2:] + "." + self.ext
                grid = helper.create_grid_from_text(text, True)
                start_matrix = helper.convert_to_matrix(
                    grid, constant.BOARD_SIZE)
                matrices_all = []
                matrices_positive = get_steps(line, start_matrix, matrices_all)
                solver = solver_bfs.SolverBfs()
                solver.output = False
                matrices_neutral = solver.solve(start_matrix)
                process_neutral(matrices_neutral,
                                matrices_positive, matrices_all)
                self.print_all_labels(matrices_all)
                if not os.path.exists(self.folder):
                    os.makedirs(self.folder)
                file_c = open(self.folder + "\\" + filename, 'w')
                try:
                    for matrix_obj in matrices_all:
                        file_c.write(
                            flatten_matrix_to_line(matrix_obj) + "\n")
                finally:
                    file_c.close()
        finally:
            file.close()

    def print_all_labels(self, matrices_all):
        """
            For debugging purposes print out the number of matrices per label
        """
        print_debug_output(
            matrices_all, "Negative", self.labels[0])
        print_debug_output(
            matrices_all, "Positive", self.labels[1])
        print_debug_output(
            matrices_all, "Neutral", self.labels[2])


def process_neutral(matrices_neutral, matrices_positive, matrices_all):
    """
        Process the 'neutral' and positive matrices to store them into matrices_all,
        so we get 3 different types of data: negative,positive and (1) neutral.
    """
    id_c = 2
    hashes = []
    for mneu in matrices_neutral:
        if not helper.generate_hash(mneu) in hashes:
            hashes.append(helper.generate_hash(mneu))
            matched = False
            for mpos in matrices_positive:
                if np.array_equal(mneu, mpos):
                    matched = True
                    matrices_all.append({"id": id_c, "pos": mneu})
            if not matched:
                matrices_all.append({"id": id_c, "neg": mneu})
            id_c += 1
    print(len(hashes))


def get_steps(line, start_matrix, matrices_all):
    """
        Execute the pre-determined correct steps on a level.
    """
    solver = solver_bfs.SolverBfs()
    solver.output = False
    steps = line.split(" ")[2]
    steps = convert_steps_to_dicts(steps)
    matrices_all.append({"id": 1, "neu": start_matrix})
    return solver.solve_steps(start_matrix, steps)


def print_debug_output(matrices_all, name, key):
    """
        Abstraction for printing out the differently indexed keys
    """
    print(name + ":" +
          str(len([t for t in matrices_all if list(t.keys())[1] == key])))


def flatten_matrix_to_line(matrix_obj):
    """
        We write out the 2d matrix to a single line we seperate with rows with ','
    """
    line = ""
    label = list(matrix_obj.keys())[1]
    matrix = matrix_obj[label]
    line += label + ":"
    for y_pos, row in enumerate(matrix):
        for x_pos, column in enumerate(row):
            line += str(int(column))
            if not x_pos == 5:
                line += ','
            if x_pos == 5 and y_pos != 5:
                line += '|'
    return line


def convert_steps_to_dicts(steps):
    """
        Used for converting the predefined know positive steps to a more convenient dataformat.
    """
    directions = {'L': constant.LEFT, 'R': constant.RIGHT,
                  'D': constant.DOWN, 'U': constant.UP}
    list_steps = steps.split(",")
    step_dicts = []
    count = 0
    for step in list_steps:
        count += 1
        chars = list(step)  # always size 3
        char = constant.LABEL[chars[0]]  # character on board/matrix
        direction = directions[chars[1]]  # direction on board/matrix
        steps = int(chars[2])  # steps in direction on board/matrix
        tmp = {"id": count, "char": char,
               "direction": direction, "steps": steps}
        step_dicts.append(tmp)
    step_dicts.sort(key=lambda x: x['id'], reverse=True)
    return step_dicts
