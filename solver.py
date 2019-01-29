"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    BFS and DFS approach implemented.
"""
import copy
import helper
import constant
from collections import deque
from timeit import default_timer as timer

class Solver:

    def __init__(self):
        self.list_visited_boards = {}
        self.stack = []
        self.queue = deque()
        self.predecessor = {}
        self.total_steps = 0
        self.output = True
        self.algo_mode = ''
        self.start_time = None
        self.end_time = None

    def solve_dfs(self, board):
        """
            Keep exploring unseen states until red vehicle is found at destination.
        """
        self.start_time = timer()
        solved = False
        self.algo_mode = 'dfs'
        self.propose_dfs(board, None)
        vehicles = self.detect_vehicles(board)
        count = 0
        goal = None
        while self.stack:
            unseen_board = self.stack.pop()
            # we have to renew the list of vehicles for each board, or we can never solve the board
            # the bread first search only works if we can explore different starting boards, derived from previous boards.
            vehicles = self.detect_vehicles(unseen_board)
            if goal != None and helper.is_win_position(goal) and not solved:
                self.end_time = timer()
                print("Found solution by evaluating " + str(count) + " different nodes!")
                self.traverse_optimal_moves(unseen_board)
                print("algo time:" + str(self.end_time - self.start_time))
                solved = True
                break
            # for each state return the red vehicle
            goal = self.explore(vehicles, unseen_board)
            count += 1
        return self.list_visited_boards

    def traverse_optimal_moves(self, end_board):
        board_hash = self.predecessor[helper.generate_hash(end_board.tostring())]
        count = 0
        while board_hash != None:
            count += 1
            #print(self.list_visited_boards[board_hash])
            board_hash = self.predecessor[board_hash]
        print("Graph consisted of " + str(count) + " steps!")
    
    def solve_bfs(self, board):
        self.start_time = timer()
        solved = False
        self.algo_mode = "bfs"
        self.propose_bfs(board, None)
        vehicles = self.detect_vehicles(board)
        count = 0
        goal = None
        while self.queue:
            unseen_board = self.queue.popleft()
            # we have to renew the list of vehicles for each board, or we can never solve the board
            # the bread first search only works if we can explore different starting boards, derived from previous boards.
            vehicles = self.detect_vehicles(unseen_board)
            if goal != None and helper.is_win_position(goal) and not solved:
                self.end_time = timer()
                print("Found solution by evaluating " + str(count) + " different nodes!")
                self.traverse_optimal_moves(unseen_board)
                print("algo time:" + str(self.end_time - self.start_time))
                solved = True
                break
            # for each state return the red vehicle
            goal = self.explore(vehicles, unseen_board)
            count += 1
        return self.list_visited_boards

    def detect_vehicles(self, board):
        vehicles = []
        for y_pos, row in enumerate(board):
            for x_pos, _ in enumerate(row):
                vehicle = helper.find_vehicle_on_board_position(board, y_pos, x_pos)
                duplicate = False
                for comp_vehicle in vehicles:
                    if vehicle is None:
                        break
                    if comp_vehicle == vehicle:
                        duplicate = True
                        break
                if not vehicle or duplicate:  # skip the same vehicle
                    continue
                vehicles.append(vehicle)
        return vehicles

    def propose_dfs(self, next_matrix, prev_matrix):
        """
            Add new hashed matrix to predeccesor dictionary if not exists,
            and add to stack for next exploration.
        """
        if not helper.generate_hash(next_matrix.tostring()) in self.predecessor:
            if prev_matrix is not None:
                prev_matrix = helper.generate_hash(prev_matrix.tostring())
            self.predecessor[helper.generate_hash(next_matrix.tostring())] = prev_matrix
            # need to copy it because python references by default.
            self.list_visited_boards[helper.generate_hash(next_matrix.tostring())] = copy.copy(next_matrix)
            self.stack.append(copy.copy(next_matrix))
            return True
        return False

    def propose_bfs(self, next_matrix, prev_matrix):
        """
            Add new hashed matrix to predeccesor dictionary if not exists,
            and add to queue for next exploration.
        """
        if not helper.generate_hash(next_matrix.tostring()) in self.predecessor:
            if prev_matrix is not None:
                prev_matrix = helper.generate_hash(prev_matrix.tostring())
            self.predecessor[helper.generate_hash(next_matrix.tostring())] = prev_matrix
            # need to copy it because python references by default.
            self.list_visited_boards[helper.generate_hash(next_matrix.tostring())] = copy.copy(next_matrix)
            self.queue.append(copy.copy(next_matrix))
            return True
        return False

    def explore(self, vehicles, board):
        """
            Scan the entire board per point for vehicles,
            making sure that each vehicle is moved only once per exploration.

            should we not find the vehicles initially and iterate over the vehicles and find empty spots.
            instead of iterating through all the points and finding vehicles and empty spots.

            one could argue when all vehicles are known, we are only interested in empty spots, in which we can move vehicles.
        """
        goal = None
        # problem is 
        for vehicle in vehicles:
            if vehicle.is_red_car():
                goal = vehicle
            
            if(vehicle.mode == 'hor'):
                count_left = {constant.LEFT: helper.count_empty_spots_in_dir(
                    board, vehicle, constant.LEFT)}
                count_right = {constant.RIGHT: helper.count_empty_spots_in_dir(
                    board, vehicle, constant.RIGHT)}
                self.slide(board, vehicle, count_left)
                self.slide(board, vehicle, count_right)
            else:
                count_up = {constant.UP: helper.count_empty_spots_in_dir(
                    board, vehicle, constant.UP)}
                count_down = {constant.DOWN: helper.count_empty_spots_in_dir(
                    board, vehicle, constant.DOWN)}
                self.slide(board, vehicle, count_up)
                self.slide(board, vehicle, count_down)
            # during explore state only one move is allowed, or we deadlock the bruteforce.
            vehicle.reset_has_moved()
        return goal
    
    def determine_allowed_move(self, board, vehicle, direction, axis, stepsize):
        allowed = False
        if direction == constant.LEFT or direction == constant.UP:
            allowed = helper.check_boundaries(vehicle.position[0][axis] + stepsize)
        elif direction == constant.RIGHT or direction == constant.DOWN:
            size_index = vehicle.size - 1
            allowed = helper.check_boundaries(vehicle.position[size_index][axis] + stepsize)
            
        if vehicle.mode == 'hor' and axis == 'y':
            allowed = False

        if vehicle.mode == 'ver' and axis == 'x':
            allowed = False

        # this is a guard that was necessary to correct for multiple movements of the same vehicle?
        # TURNS out we still want one vehicle movement per exploration of the board.
        if stepsize == 0 or vehicle.has_moved:
           allowed = False

        # check allowed or we are already out of bounds
        if allowed and not helper.is_board_position_empty_in_direction(board, vehicle, direction):
            allowed = False

        return allowed
    
    def slider(self, board, vehicle, direction, axis, stepsize):
        """
            Slide on empty spots depending on vehicle size and direction
        """

        allowed = self.determine_allowed_move(board, vehicle, direction, axis, stepsize)

        if allowed:
            self.total_steps += 1
            # if self.output:
            #     print(str(vehicle.identifier) + "-" + direction)
            vehicle.drive(axis, stepsize)
            return True
        return False

    def slide(self, board, vehicle, direction):
        """
            Derive the axis from the direction and determine of stepsize is negative or positive
        """
        if not vehicle.has_moved:
            # copy in order to generate correct hash
            current_board = copy.copy(board)
            # for multi level object deep copy!
            old_position = copy.deepcopy(vehicle.position)  
            dir_key = list(direction.keys())[0]
            stepsize = direction[dir_key]
            direction_axis_mapping = {
                constant.UP: 'y', 
                constant.DOWN: 'y',
                constant.LEFT: 'x', 
                constant.RIGHT: 'x'}
            if dir_key == constant.LEFT or dir_key == constant.UP:
                stepsize = -stepsize
            self.slider(board, vehicle, dir_key, direction_axis_mapping[dir_key], stepsize)
            self.update_board(board, vehicle, old_position)
            if(self.algo_mode == 'dfs'):
                unseen_result = self.propose_dfs(board, current_board)
            else:
                unseen_result = self.propose_bfs(board, current_board)
            # if unseen_result:
            #     print(board)  # unique moves
            #     print("-----------------")

    def update_board(self, board, vehicle, old_position):
        """
            Update the rush hour board with new vehicle positions, and update vehicle to the new position
        """
        if(vehicle.has_moved):
            for block, _ in enumerate(old_position):
                board[old_position[block]['y'], old_position[block]['x']] = 0
            for block, _ in enumerate(vehicle.position):
                board[vehicle.position[block]['y'], vehicle.position[block]['x']] = vehicle.identifier

# Data dump methods using BFS method.

    def solve_steps(self, start_matrix, steps):
        """
            Execute the steps given on the starting matrix.
        """
        solved = False
        self.propose_bfs(start_matrix, None)
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
            self.propose_bfs(board, next_board)
        if vehicle and vehicle.is_red_car():
            red = vehicle
        return red

