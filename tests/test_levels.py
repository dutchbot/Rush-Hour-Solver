"""
    Holds test classes and their respective methods.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from rushhour import constant
from rushhour import helper
from rushhour.solver import solver_bfs


class TestLevels(unittest.TestCase):
    """
        Contains test method(s) for testing levels.
    """

    def test_levels_from_file(self):
        """
            Test the levels from files, assert if all levels were solved.
        """
        file_name = open('levels.txt', 'r')
        count = 0
        count_solved = 0

        try:
            for line in file_name.readlines():
                main = solver_bfs.SolverBfs()
                main.output = False
                text = line.split(" ")[0]
                grid = helper.create_grid_from_text(text, True)
                matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
                if main.solve(matrix):
                    count_solved += 1
                count += 1
                print(main.total_steps)
                main.total_steps = 0
        finally:
            file_name.close()
        self.assertEqual(count, count_solved)
