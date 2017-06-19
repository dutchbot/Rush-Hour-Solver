"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    In a bruteforce manner, BFS approach.
"""
import copy
import numpy
import helper
import constant
from vehicle_detector import VehicleDetector2, VehicleDetector3
from vehicle import Vehicle


class Solver:
    """
        Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
        In a bruteforce manner, BFS approach.
    """

    def __init__(self):
        self.list_matrices_full = []
        self.queue = []
        self.predecessor = {}
        self.total_steps = 0
        self.output = True

    def propose(self, next_matrix, prev_matrix):
        """
            Add new hashed matrix to predeccesor dictionary if not exists,
            and add to queue for next exploration.
        """
        if not self.generate_hash(next_matrix) in self.predecessor:
            if prev_matrix is not None:
                prev_matrix = self.generate_hash(prev_matrix)
            self.predecessor[self.generate_hash(next_matrix)] = prev_matrix
            # need to copy it because python references by default.
            self.list_matrices_full.append(copy.copy(next_matrix))
            self.queue.append(copy.copy(next_matrix))
            return True
        return False

    def solve(self, start_matrix):
        """
            Keep exploring unseen states until red vehicle is found at destination.
        """
        solved = False
        self.propose(start_matrix, None)
        count = 0
        red = None
        while self.queue:
            current = self.queue.pop()  # take a new matrix from the queue
            if red != None and self.is_win_position(red) and not solved:
                print("Found solution in " + str(count) + " steps!")
                print(current)
                solved = True
                break
            # for each state return the red vehicle
            red = self.explore(current)
            count += 1
        return self.list_matrices_full

    def solve_steps(self, start_matrix, steps):
        """
            Execute the steps given on the starting matrix.
        """
        solved = False
        self.propose(start_matrix, None)
        step_length = len(steps)
        count = 0
        red = None
        while self.queue:
            current = self.queue.pop()  # take a new matrix from the queue
            if red != None and self.is_win_position(red) and not solved:
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
                    red = self.try_to_find_vehicle_c(current, step)
                if red.position[1]['x'] < 5:
                    step['steps'] = 5 - red.position[1]['x']
                red = self.do_step(current, step)
            count += 1
        return self.list_matrices_full

    def do_step(self, matrix, step):
        """
            do a pre determined step
        """
        red = None
        vehicle = self.try_to_find_vehicle_c(matrix, step)
        test = {constant.UP: 'y', constant.DOWN: 'y',
                constant.LEFT: 'x', constant.RIGHT: 'x'}
        new_matrix = copy.copy(
            matrix)  # copy in order to generate correct hash
        if vehicle:
            dir_key = step['direction']
            stepsize = step['steps']
            if dir_key == constant.LEFT or dir_key == constant.UP:
                stepsize = -stepsize
            self.slider(matrix, vehicle, dir_key, test[dir_key], stepsize)
            self.update_matrix(matrix, vehicle)
            self.propose(matrix, new_matrix)
        if vehicle and vehicle.is_red_car():
            red = vehicle
        return red

    def is_win_position(self, vehicle):
        """
            Checks for the static size coordinates and correct character.
        """
        if vehicle.is_red_car() and vehicle.position[0]['x'] == 4 and vehicle.position[1]['x'] == 5:
            return True

    def try_to_find_vehicle_c(self, matrix, step):
        """
            Find vehicles either horizontal or vertical, both is not possible at the same position.
        """
        for y_pos, row in enumerate(matrix):
            for x_pos, column in enumerate(row):
                if step['direction'] == constant.LEFT or step['direction'] == constant.RIGHT:
                    vehicle = self.find_vehicle_bounds(
                        matrix, y_pos, x_pos, 'hor')
                else:
                    vehicle = self.find_vehicle_bounds(
                        matrix, y_pos, x_pos, 'ver')

                if vehicle and vehicle.char == step['char']:
                    return vehicle
        return None

    def explore(self, matrix):
        """
            Scan the entire matrix per point for vehicles,
            making sure that each vehicle is moved only once per exploration.
        """
        red = None
        vehicles = []
        for y_pos, row in enumerate(matrix):
            for x_pos, column in enumerate(row):
                vehicle = self.try_to_find_vehicle(matrix, y_pos, x_pos)
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
                if vehicle.is_red_car():
                    red = vehicle
                count_left = {constant.LEFT: self.count_empty_spots_in_dir(
                    matrix, vehicle, constant.LEFT)}
                count_right = {constant.RIGHT: self.count_empty_spots_in_dir(
                    matrix, vehicle, constant.RIGHT)}
                count_up = {constant.UP: self.count_empty_spots_in_dir(
                    matrix, vehicle, constant.UP)}
                count_down = {constant.DOWN: self.count_empty_spots_in_dir(
                    matrix, vehicle, constant.DOWN)}
                self.slide(matrix, vehicle, count_left)
                self.slide(matrix, vehicle, count_right)
                self.slide(matrix, vehicle, count_up)
                self.slide(matrix, vehicle, count_down)
        return red

    def count_empty_spots_in_dir(self, matrix, vehicle, direction):
        """
            When count_empty is incremented the position values increment or decrement,
            according to direction and horizontal/vertical mode.
            Thus deriving the empty spots in a given direction.
        """
        count_empty = 1  # in order for multiplier to work
        x_pos = vehicle.position[0]['x']
        y_pos = vehicle.position[0]['y']
        if direction == constant.LEFT:
            offset_hor = -1
            offset_ver = 0
        elif direction == constant.RIGHT:
            if vehicle.size == 2:
                x_pos = vehicle.position[1]['x']
                y_pos = vehicle.position[1]['y']
            else:
                x_pos = vehicle.position[2]['x']
                y_pos = vehicle.position[2]['y']
            offset_hor = 1
            offset_ver = 0
        elif direction == constant.UP:
            offset_hor = 0
            offset_ver = -1
        elif direction == constant.DOWN:
            if vehicle.size == 2:
                x_pos = vehicle.position[1]['x']
                y_pos = vehicle.position[1]['y']
            else:
                x_pos = vehicle.position[2]['x']
                y_pos = vehicle.position[2]['y']
            offset_hor = 0
            offset_ver = 1

        while self.check_valid(matrix, y_pos, x_pos, offset_ver, offset_hor, count_empty):
            count_empty += 1
        if count_empty == 1:
            return 0
        else:
            return count_empty - 1

    def check_valid(self, matrix, y, x, offset_ver, offset_hor, count_empty):
        """
            Boundary check and if spot is empty
        """
        y_pos = y + offset_ver * count_empty
        x_pos = x + offset_hor * count_empty
        return helper.check_boundaries(y_pos) and \
            helper.check_boundaries(x_pos) and \
            matrix[y_pos, x_pos] == 0

    def try_to_find_vehicle(self, matrix, y_pos, x_pos):
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

    def find_vehicle_bounds(self, matrix, y_pos, x_pos, mode):
        """
            Detect the start and end point of vehicles depending on size,
            we can either have a size of 2 or 3 at a given spot not both.
        """
        current = matrix[y_pos, x_pos]
        vehicle = Vehicle()
        vehicle.char = current
        if current != 0:
            size_3 = VehicleDetector3().find_vehicle(
                matrix, y_pos, x_pos, mode, vehicle, current)
            if size_3:
                return size_3
            size_2 = VehicleDetector2().find_vehicle(
                matrix, y_pos, x_pos, mode, vehicle, current)
            if size_2:
                return size_2
        return None

    def create_grid_from_text(self, text, file=False):
        """
            Convert textual representation to numerical representation
        """
        if file:
            grid = text.split("\\n")
        else:
            grid = text.split("\n")
        for idx, row in enumerate(grid):
            grid[idx] = list(row)

        indexes = list()
        county = 0
        for row in grid:
            countx = 0
            for position in row:
                indexes.append(
                    {'char': constant.LABEL[position], 'y': county, 'x': countx})
                countx += 1
            county += 1

        if constant.DEBUG == 1:
            print(len(indexes))

        return indexes

    def convert_to_matrix(self, grid, size):
        """
            Convert text string to numerical matrix
        """
        matrix = numpy.zeros(shape=(size, size))
        for position in grid:
            matrix[position['y'], position['x']] = position['char']
        if constant.DEBUG == 1:
            print(matrix)
        return matrix

    # look at object boundaries/size
    def test_neighbour_empty(self, matrix, vehicle, direction):
        """
            Look if next position relative to vehicle size is empty spot
        """
        if direction == constant.LEFT:
            return self.get_valid_move(matrix, vehicle, 0, 0, -1)
        elif direction == constant.RIGHT:
            if vehicle.size == 2:
                return self.get_valid_move(matrix, vehicle, 1, 0, 1)
            else:
                return self.get_valid_move(matrix, vehicle, 2, 0, 1)
        elif direction == constant.UP:
            return self.get_valid_move(matrix, vehicle, 0, -1, 0)
        elif direction == constant.DOWN:
            if vehicle.size == 2:
                return self.get_valid_move(matrix, vehicle, 1, 1, 0)
            else:
                return self.get_valid_move(matrix, vehicle, 2, 1, 0)

        return False

    def get_valid_move(self, matrix, vehicle, index, offset, offset_hor):
        """
            Check if move falls within bounderies and if spot is empty
        """
        y_pos = vehicle.position[index]['y'] + offset
        x_pos = vehicle.position[index]['x'] + offset_hor
        return helper.check_boundaries(y_pos) and \
            helper.check_boundaries(x_pos) and \
            matrix[y_pos][x_pos] == 0

    def generate_hash(self, matrix):
        """
            Generate hash based on 2d array contents
        """
        return hash(matrix.tostring())

    def slide(self, matrix, vehicle, direction):
        """
            Derive the axis from the direction and determine of stepsize is negative or positive
        """
        new_matrix = copy.copy(
            matrix)  # copy in order to generate correct hash
        dir_key = list(direction.keys())[0]
        stepsize = direction[dir_key]
        test = {constant.UP: 'y', constant.DOWN: 'y',
                constant.LEFT: 'x', constant.RIGHT: 'x'}
        if dir_key == constant.LEFT or dir_key == constant.UP:
            stepsize = -stepsize
        self.slider(matrix, vehicle, dir_key, test[dir_key], stepsize)
        self.update_matrix(matrix, vehicle)
        val = self.propose(matrix, new_matrix)
        if val and constant.DEBUG == 1:
            print(matrix)  # unique moves
            print("-----------------")
        return False

    def slider(self, matrix, vehicle, direction, plc, stepsize):
        """
            Slide on empty spots depending on vehicle size and direction
        """
        vehicle.init_new_pos()
        allowed = False
        if direction == constant.LEFT or direction == constant.UP:
            allowed = helper.check_boundaries(
                vehicle.new_positions[0][plc] + stepsize)
        elif direction == constant.RIGHT or direction == constant.DOWN:
            if vehicle.size == 3:
                allowed = helper.check_boundaries(
                    vehicle.new_positions[2][plc] + stepsize)
            else:
                allowed = helper.check_boundaries(
                    vehicle.new_positions[1][plc] + stepsize)
        if vehicle.mode == 'hor' and plc == 'y':
            allowed = False

        if vehicle.mode == 'ver' and plc == 'x':
            allowed = False

        if stepsize == 0 or vehicle.move_count == 1:
            allowed = False

        # check allowed or we are already out of bounds
        if allowed and not self.test_neighbour_empty(matrix, vehicle, direction):
            allowed = False

        if allowed:
            self.total_steps += 1
            if self.output:
                print(str(vehicle.char) + "-" + direction)
            vehicle.new_positions[0][plc] += stepsize
            vehicle.new_positions[1][plc] += stepsize
            if vehicle.size == 3:
                vehicle.new_positions[2][plc] += stepsize
            vehicle.move_count += 1
            return True
        return False

    def update_matrix(self, matrix, vehicle):
        """
            Update the matrix with new vehicle positions, and update vehicle to the new position
        """
        if vehicle.new_positions:
            matrix[vehicle.position[0]['y'],
                   vehicle.position[0]['x']] = 0
            matrix[vehicle.position[1]['y'],
                   vehicle.position[1]['x']] = 0
            if vehicle.size == 3:
                matrix[vehicle.position[2]['y'],
                       vehicle.position[2]['x']] = 0
            matrix[vehicle.new_positions[0]['y'],
                   vehicle.new_positions[0]['x']] = vehicle.char
            matrix[vehicle.new_positions[1]['y'],
                   vehicle.new_positions[1]['x']] = vehicle.char
            if vehicle.size == 3:
                matrix[vehicle.new_positions[2]['y'],
                       vehicle.new_positions[2]['x']] = vehicle.char
            vehicle.update_current_position()
