"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    In a bruteforce manner, BFS approach.
"""
import copy
import helper
import constant


class Solver2:

    def __init__(self):
        self.list_matrices_full = []
        self.queue = []
        self.predecessor = {}
        self.total_steps = 0
        self.output = True

    def solve(self, board):
        """
            Keep exploring unseen states until red vehicle is found at destination.
        """
        solved = False
        self.propose(board, None)
        vehicles = self.detect_vehicles(board)
        count = 0
        goal = None
        while self.queue:
            current = self.queue.pop()  # take a new matrix from the queue
            if goal != None and helper.is_win_position(goal) and not solved:
                print("Found solution in " + str(count) + " steps!")
                print(current)
                solved = True
                break
            # for each state return the red vehicle
            goal = self.explore(vehicles, current)
            count += 1
        return self.list_matrices_full

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

    def propose(self, next_matrix, prev_matrix):
        """
            Add new hashed matrix to predeccesor dictionary if not exists,
            and add to queue for next exploration.
        """
        if not helper.generate_hash(next_matrix) in self.predecessor:
            if prev_matrix is not None:
                prev_matrix = helper.generate_hash(prev_matrix)
            self.predecessor[helper.generate_hash(next_matrix)] = prev_matrix
            # need to copy it because python references by default.
            self.list_matrices_full.append(copy.copy(next_matrix))
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
            if self.output:
                print(str(vehicle.identifier) + "-" + direction)
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
            unseen_result = self.propose(board, current_board)
            if unseen_result:
                print(board)  # unique moves
                print("-----------------")

    def update_board(self, board, vehicle, old_position):
        """
            Update the rush hour board with new vehicle positions, and update vehicle to the new position
        """
        for block, _ in enumerate(old_position):
            board[old_position[block]['y'], old_position[block]['x']] = 0
        for block, _ in enumerate(vehicle.position):
            board[vehicle.position[block]['y'], vehicle.position[block]['x']] = vehicle.identifier

