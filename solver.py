"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    BFS and DFS approach implemented.
"""
import copy
import helper
import constant
from collections import deque
from timeit import default_timer as timer

class SolverOld:
   
# Data dump methods using BFS method.

    def solve_steps(self, start_matrix, steps):
        """
            Execute the steps given on the starting matrix.
        """
        solved = False
        self.propose(start_matrix, None, self.queue)
        step_length = len(steps)
        count = 0
        red = None
        while self.queue:
            current = self.queue.pop()  # take a new matrix from the queue
            if red != None and helper.is_win_position(red) and not solved:
                print("Found solution in " + str(count) + " steps!")
                solved = True
                break
            if count != step_length - 1:
                step = steps.pop()  # after check pls
                # for each state return the red vehicle
                red = self.do_step(current, step)
            else:  # fixing the difference between digital and board
                step = steps.pop()
                if red is None:  # dirty
                    red = helper.find_vehicle_axis(current, step)
                if red.position[1]['x'] < 5:
                    step['steps'] = 5 - red.position[1]['x']
                red = self.do_step(current, step)
            count += 1
        return self.list_visited_boards

    def do_step(self, board, step):
        """
            do a pre determined step
        """
        red = None
        vehicle = helper.find_vehicle_axis(board, step)
        old_position = copy.deepcopy(vehicle.position) 
        test = {constant.UP: 'y', constant.DOWN: 'y',
                constant.LEFT: 'x', constant.RIGHT: 'x'}
        # copy in order to generate correct hash
        next_board = copy.copy(board) 
        if vehicle:
            dir_key = step['direction']
            stepsize = step['steps']
            if dir_key == constant.LEFT or dir_key == constant.UP:
                stepsize = -stepsize
            self.slider(board, vehicle, dir_key, test[dir_key], stepsize)
            self.update_board(board, vehicle, old_position)
            self.propose(board, next_board, self.queue)
        if vehicle and vehicle.is_red_car():
            red = vehicle
        return red

