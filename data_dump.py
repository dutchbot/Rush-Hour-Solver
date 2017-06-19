"""
    Contains the data dump class to dump rush hour steps (matrices) to a file.
"""

import constant
from solver import Solver
import numpy as np


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
                solver = Solver()
                solver.output = False
                text = line.split(" ")[0]
                filename = "lvl" + line.split(" ")[1][-2:] + "." + self.ext
                grid = solver.create_grid_from_text(text, True)
                start_matrix = solver.convert_to_matrix(
                    grid, constant.BOARD_SIZE)
                steps = line.split(" ")[2]
                steps = self.convert_steps_to_dicts(steps)
                matrices_all = []
                matrices_all.append({"id": 1, "neu": start_matrix})
                matrices_positive = solver.solve_steps(start_matrix, steps)
                solver = Solver()
                solver.output = False
                matrices_neutral = solver.solve(start_matrix)
                id_c = 2
                hashes = []
                for mneu in matrices_neutral:
                    if not solver.generate_hash(mneu) in hashes:
                        hashes.append(solver.generate_hash(mneu))
                        matched = False
                        for mpos in matrices_positive:
                            if np.array_equal(mneu, mpos):
                                matched = True
                                matrices_all.append({"id": id_c, "pos": mneu})
                        if not matched:
                            matrices_all.append({"id": id_c, "neg": mneu})
                        id_c += 1
                print(len(hashes))
                self.print_debug_output(
                    matrices_all, "Negative", self.labels[0])
                self.print_debug_output(
                    matrices_all, "Positive", self.labels[1])
                self.print_debug_output(
                    matrices_all, "Neutral", self.labels[2])
                file_c = open(self.folder + "\\" + filename, 'w')
                try:
                    for matrix_obj in matrices_all:
                        file_c.write(
                            self.flatten_matrix_to_line(matrix_obj) + "\n")
                finally:
                    file_c.close()
        finally:
            file.close()

    def print_debug_output(self, matrices_all, name, key):
        """
            Abstraction for printing out the differently indexed keys
        """
        print(name + ":" +
              str(len([t for t in matrices_all if list(t.keys())[1] == key])))

    def flatten_matrix_to_line(self, matrix_obj):
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

    def convert_steps_to_dicts(self, steps):
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


DATA_DUMP = DataDump()
DATA_DUMP.dump_data_to_file()
