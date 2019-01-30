import copy
import helper
import rush_hour

class SolverDfs:

    def __init__(self):
        self.visited_boards = {}
        self.stack = []
        self.predecessor = {}
        self.solved = False

    def propose_easy(self, next_matrix, prev_matrix):
        return helper.propose(self.predecessor, self.visited_boards, next_matrix, prev_matrix, self.stack)

    def solve(self, board):
        self.propose_easy(board, None)
        playgame = rush_hour.RushHour(self.propose_easy)
        while self.stack:
            unseen_board = self.stack.pop()
            if playgame.play(unseen_board):
                helper.traverse_optimal_moves(self.predecessor, unseen_board)
                self.solved = True
                break
        if not self.solved:
            print("Did not find solution..")
        return self.visited_boards