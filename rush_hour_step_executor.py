"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    BFS and DFS approach implemented.
"""
import copy
import helper
import constant
from collections import deque
from timeit import default_timer as timer
import rush_hour
import game_helper

class RushHourStepExecutor(rush_hour.RushHour):
   
# Data dump methods using BFS method.

    def __init__(self):
        super(RushHourStepExecutor, self).__init__()
        self.steps = []

    def play(self, board, steps):
        """
            Execute the steps given on the starting matrix.
        """
        count = 0
        step_length = len(steps)
        if self.goal != None and self.is_win_position(self.goal) and not self.solved:
            print("Found solution in " + str(count) + " steps!")
            self.solved = True
        if count != step_length - 1:
            if(step_length == 0):
                return
            step = steps.pop()
            # for each state return the red vehicle
            self.goal = self.do_step(board, step)
        else:  # fixing the difference between digital and board
            step = steps.pop()
            if self.goal is None:  # dirty
                self.goal = game_helper.find_vehicle_axis(board, step)
            if self.goal.position[1]['x'] < 5:
                step['steps'] = 5 - self.goal.position[1]['x']
            self.goal = self.do_step(board, step)
        count += 1


    def do_step(self, board, step):
        """
            do a pre determined step
        """
        red = None
        vehicle = game_helper.find_vehicle_axis(board, step)
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
            self.propose_easy(board, next_board)
        if vehicle and vehicle.is_red_car():
            red = vehicle
        return red

