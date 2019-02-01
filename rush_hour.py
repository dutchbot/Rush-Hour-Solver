import copy
import helper
import constant
from timeit import default_timer as timer
from vehicle_detector import VehicleDetector
from vehicle import Vehicle


class RushHour():

    def __init__(self, propose_easy):
        self.solved = False
        self.explored_boards = 0
        self.start_time = timer()
        self.end_time = None
        # type vehicle
        self.goal = None
        self.total_steps = 0
        self.propose_easy = propose_easy

    def play(self, unseen_board):
        # we have to renew the list of vehicles for each board, or we can never solve the board
        # the bread first search only works if we can explore different starting boards, derived from previous boards.
        vehicles = self.detect_vehicles(unseen_board)
        if self.goal != None and self.is_win_position(self.goal) and not self.solved:
            self.end_time = timer()
            print("Found solution by evaluating " +
                  str(self.explored_boards) + " different nodes!")
            print("algo time:" + str(self.end_time - self.start_time))
            self.solved = True
            return True
        # for each state return the red vehicle
        self.goal = self.explore(vehicles, unseen_board)
        self.explored_boards += 1
        return False

    def detect_vehicles(self, board):
        vehicles = []
        for y_pos, row in enumerate(board):
            for x_pos, _ in enumerate(row):
                vehicle = self.find_vehicle_on_board_position(
                    board, y_pos, x_pos)
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

    def explore(self, vehicles, board):
        """
            Scan the entire board per point for vehicles,
            making sure that each vehicle is moved only once per exploration.

            should we not find the vehicles initially and iterate over the vehicles and find empty spots.
            instead of iterating through all the points and finding vehicles and empty spots.

            one could argue when all vehicles are known, we are only interested in empty spots, in which we can move vehicles.
        """
        goal = None
        for vehicle in vehicles:
            if vehicle.is_red_car():
                goal = vehicle

            if(vehicle.mode == 'hor'):
                count_left = {constant.LEFT: self.count_empty_spots_in_dir(
                    board, vehicle, constant.LEFT)}
                count_right = {constant.RIGHT: self.count_empty_spots_in_dir(
                    board, vehicle, constant.RIGHT)}
                self.slide(board, vehicle, count_left)
                self.slide(board, vehicle, count_right)
            else:
                count_up = {constant.UP: self.count_empty_spots_in_dir(
                    board, vehicle, constant.UP)}
                count_down = {constant.DOWN: self.count_empty_spots_in_dir(
                    board, vehicle, constant.DOWN)}
                self.slide(board, vehicle, count_up)
                self.slide(board, vehicle, count_down)
            # during explore state only one move is allowed, or we deadlock the bruteforce.
            vehicle.reset_has_moved()
        return goal

    def determine_allowed_move(self, board, vehicle, direction, axis, stepsize):
        allowed = False
        if direction == constant.LEFT or direction == constant.UP:
            allowed = self.check_boundaries(
                vehicle.position[0][axis] + stepsize)
        elif direction == constant.RIGHT or direction == constant.DOWN:
            size_index = vehicle.size - 1
            allowed = self.check_boundaries(
                vehicle.position[size_index][axis] + stepsize)

        if vehicle.mode == 'hor' and axis == 'y':
            allowed = False

        if vehicle.mode == 'ver' and axis == 'x':
            allowed = False

        # this is a guard that was necessary to correct for multiple movements of the same vehicle?
        # TURNS out we still want one vehicle movement per exploration of the board.
        if stepsize == 0 or vehicle.has_moved:
            allowed = False

        # check allowed or we are already out of bounds
        if allowed and not self.is_board_position_empty_in_direction(board, vehicle, direction):
            allowed = False

        return allowed

    def slider(self, board, vehicle, direction, axis, stepsize):
        """
            Slide on empty spots depending on vehicle size and direction
        """

        allowed = self.determine_allowed_move(
            board, vehicle, direction, axis, stepsize)

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
            previous_board = copy.deepcopy(board)
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
            self.slider(board, vehicle, dir_key,
                        direction_axis_mapping[dir_key], stepsize)
            self.update_board(board, vehicle, old_position)
            unseen_result = self.propose_easy(board, previous_board)
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
                board[vehicle.position[block]['y'],
                      vehicle.position[block]['x']] = vehicle.identifier

    def is_win_position(self, vehicle):
        """
            Checks for the static size coordinates and correct character.
        """
        if vehicle.is_red_car() and vehicle.position[0]['x'] == 4 and vehicle.position[1]['x'] == 5:
            return True
        return False

    def check_valid_move(self, matrix, vehicle, index, offset, offset_hor):
        """
            Check if move falls within boundaries and if spot is empty
        """
        y_pos = vehicle.position[index]['y'] + offset
        x_pos = vehicle.position[index]['x'] + offset_hor
        return self.check_boundaries(y_pos) and \
            self.check_boundaries(x_pos) and \
            matrix[y_pos][x_pos] == 0

        # look at object boundaries/size
    def is_board_position_empty_in_direction(self, matrix, vehicle, direction):
        """
            Look if next position relative to vehicle size is empty spot
        """
        if direction == constant.LEFT:
            return self.check_valid_move(matrix, vehicle, 0, 0, -1)
        elif direction == constant.RIGHT:
            if vehicle.size == 2:
                return self.check_valid_move(matrix, vehicle, 1, 0, 1)
            else:
                return self.check_valid_move(matrix, vehicle, 2, 0, 1)
        elif direction == constant.UP:
            return self.check_valid_move(matrix, vehicle, 0, -1, 0)
        elif direction == constant.DOWN:
            if vehicle.size == 2:
                return self.check_valid_move(matrix, vehicle, 1, 1, 0)
            else:
                return self.check_valid_move(matrix, vehicle, 2, 1, 0)

        return False

    def count_empty_spots_in_dir(self, matrix, vehicle, direction):
        """
            When count_empty is incremented the position values increment or decrement,
            according to direction and horizontal/vertical mode.
            Thus deriving the empty spots in a given direction.
        """
        count_empty = 1  # in order for multiplier to work
        indexed_size = vehicle.size - 1

        DIRECTIONS = {constant.LEFT: {
            "x": vehicle.position[0]['x'],
            "y": vehicle.position[0]['y'],
            "offset_hor": -1,
            "offset_ver": 0},
            constant.RIGHT: {
            "x": vehicle.position[indexed_size]['x'],
            "y": vehicle.position[indexed_size]['y'],
            "offset_hor": 1,
            "offset_ver": 0},
            constant.UP: {
            "x": vehicle.position[0]['x'],
            "y": vehicle.position[0]['y'],
            "offset_hor": 0,
            "offset_ver": -1},
            constant.DOWN: {
            "x": vehicle.position[indexed_size]['x'],
            "y": vehicle.position[indexed_size]['y'],
            "offset_hor": 0,
            "offset_ver": 1}
        }

        y_pos = DIRECTIONS[direction]["y"]
        x_pos = DIRECTIONS[direction]["x"]
        offset_ver = DIRECTIONS[direction]["offset_ver"]
        offset_hor = DIRECTIONS[direction]["offset_hor"]

        while self.check_valid_lane(matrix, y_pos, x_pos, offset_ver * count_empty, offset_hor * count_empty):
            count_empty += 1
        if count_empty == 1:
            return 0
        else:
            return count_empty - 1

    def find_vehicle_on_board_position(self, matrix, y_pos, x_pos):
        """
            Find vehicles either horizontal or vertical, both is not possible at the same position.
        """
        if matrix[y_pos, x_pos] != 0:
            hor_vehicle = self.find_vehicle_bounds(matrix, y_pos, x_pos, 'hor')
            ver_vehicle = self.find_vehicle_bounds(matrix, y_pos, x_pos, 'ver')
            if ver_vehicle:
                return ver_vehicle
            if hor_vehicle:
                return hor_vehicle

    def determine_axis_by_direction(self, direction):
        if direction == constant.LEFT or direction == constant.RIGHT:
            return constant.MOVEMENT_DIRECTIONS[0]
        else:
            return constant.MOVEMENT_DIRECTIONS[1]

    def find_vehicle_axis(self, matrix, step):
        """
            Find vehicles either horizontal or vertical, both is not possible at the same position.

            This function will probably become obsolete when we move on the grid by vehicle only (OOP)
        """
        for y_pos, row in enumerate(matrix):
            for x_pos, column in enumerate(row):
                axis = self.determine_axis_by_direction(step['direction'])
                vehicle = self.find_vehicle_bounds(matrix, y_pos, x_pos, axis)
                if vehicle and vehicle.identifier == step['char']:
                    return vehicle
        return None

    def find_vehicle_bounds(self, matrix, y_pos, x_pos, mode):
        """
            Detect the start and end point of vehicles depending on size,
            we can either have a size of 2 or 3 at a given spot not both.
            on the y,x position currently selected if char > 0 try to find a vehicle of maximum size 3
        """
        vehicle_identifier = matrix[y_pos, x_pos]
        vehicle = Vehicle()
        vehicle.identifier = vehicle_identifier
        if vehicle_identifier != 0:
            size_2 = VehicleDetector().find_vehicle(
                matrix, y_pos, x_pos, mode, vehicle, vehicle_identifier)
            if size_2:
                return size_2
        return None

    def check_boundaries(self, number):
        """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
        if number < constant.BOARD_SIZE and number >= 0:
            return True
        return False

    def check_valid_lane(self, matrix, y, x, offset_ver, offset_hor):
        """
            Boundary check and if spot is empty
        """
        y_pos = y + offset_ver
        x_pos = x + offset_hor
        return self.check_boundaries(y_pos) and \
            self.check_boundaries(x_pos) and \
            matrix[y_pos, x_pos] == 0
