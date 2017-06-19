"""
    Holds test classes and their respective methods.
"""

import unittest
from main import Solver
import constant


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
                main = Solver()
                main.output = False
                print(type(line.split(" ")[0]))
                text = line.split(" ")[0]
                print(line.split(" ")[1])
                grid = main.create_grid_from_text(text, True)
                matrix = main.convert_to_matrix(grid, constant.BOARD_SIZE)
                if main.solve(matrix):
                    count_solved += 1
                count += 1
                print(main.total_steps)
                main.total_steps = 0
        finally:
            file_name.close()
        self.assertEqual(count, count_solved)


if __name__ == '__main__':
    unittest.main()
