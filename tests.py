"""
    Holds test classes and their respective methods.
"""

import unittest
from bfs import SolverBfs as Solver
import constant
import helper


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
                text = line.split(" ")[0]
                grid = helper.create_matrix_from_text(text, True)
                board = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
                print(board)
                if main.solve(board):
                    count_solved += 1
                count += 1
        except Exception as e:
            print(f"exception was raised: {e.__str__()}")
        finally:
            file_name.close()
            self.assertEqual(count, count_solved, msg="Not all levels were solved!")
            input("Press Enter to continue...")


if __name__ == '__main__':
    unittest.main()
