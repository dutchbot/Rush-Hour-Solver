""" Test the different algorithmic approaches """
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from rushhour import constant
from rushhour import helper
from rushhour import node
from rushhour.solver import solver_bfs, solver_astar


class TestAlgorithmSpeed(unittest.TestCase):
    """
        Test the speed..
    """
    def test_bfs_solver(self):
        """
            Runs the standard provided level
        """
        text = "....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"
        grid = helper.create_grid_from_text(text)
        start_matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
        self.get_solver(start_matrix, 'bfs')

    def test_astar_solver(self):
        """
            Runs the standard provided level
        """
        text = "....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"
        grid = helper.create_grid_from_text(text)
        start_matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
        self.get_solver(start_matrix, 'astar')

    def get_solver(self, start_matrix, solver):
        """
            Get the solver for differente algo's in the correct way
        """
        if solver == 'bfs':
            solver = solver_bfs.SolverBfs()
            solver.solve(start_matrix)
        else:
            solution = "AA....\nBB..CC\n....rr\nGGHHEF\n...IEF\n.JJIEF"
            grid = helper.create_grid_from_text(solution)
            goal_matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
            start = node.Node(start_matrix)
            goal = node.Node(goal_matrix)
            solver = solver_astar.SolverAstar()
            solver.solve(start, goal)
