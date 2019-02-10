import copy
import helper
import rush_hour
import numpy as np

class SolverDfs:

    def __init__(self, playgame):
        self.visited_boards = {}
        self.visited_boards_matrix = []
        self.stack = []
        self.predecessor = {}
        self.solved = False
        self.playgame = playgame

    def propose_easy(self, next_matrix, prev_matrix):
        result = helper.propose(self.predecessor, self.visited_boards, next_matrix, prev_matrix, self.stack)
        if isinstance(result, np.ndarray):
            self.visited_boards_matrix.append(result)

    def solve(self, board):
        self.propose_easy(board, None)
        self.playgame.propose_easy = self.propose_easy
        while self.stack:
            unseen_board = self.stack.pop()
            if self.playgame.play(unseen_board):
                helper.traverse_optimal_moves(self.predecessor, unseen_board)
                self.solved = True
                break
        if not self.solved:
            print("Did not find solution..")
        return self.visited_boards_matrix

    def solve_steps(self, board, steps):
        count_dict = {'count' : 0}
        self.propose_easy(board, None)
        self.playgame.propose_easy = self.propose_easy
        while self.stack:
            unseen_board = self.stack.pop()
            if self.playgame.play(unseen_board, steps, count_dict):
                helper.traverse_optimal_moves(self.predecessor, unseen_board)
                self.solved = True
                break
        if not self.solved:
            print("Did not find solution..")
        return self.visited_boards_matrix