"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    In a bruteforce manner, BFS approach.
"""
import copy
import helper
import constant


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
        if not helper.generate_hash(next_matrix) in self.predecessor:
            if prev_matrix is not None:
                prev_matrix = helper.generate_hash(prev_matrix)
            self.predecessor[helper.generate_hash(next_matrix)] = prev_matrix
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
            if red != None and helper.is_win_position(red) and not solved:
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
                    red = helper.try_to_find_vehicle_c(current, step)
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
        vehicle = helper.try_to_find_vehicle_c(matrix, step)
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

    def explore(self, matrix):
        """
            Scan the entire matrix per point for vehicles,
            making sure that each vehicle is moved only once per exploration.
        """
        red = None
        vehicles = []
        for y_pos, row in enumerate(matrix):
            for x_pos, column in enumerate(row):
                vehicle = helper.try_to_find_vehicle(matrix, y_pos, x_pos)
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
                count_left = {constant.LEFT: helper.count_empty_spots_in_dir(
                    matrix, vehicle, constant.LEFT)}
                count_right = {constant.RIGHT: helper.count_empty_spots_in_dir(
                    matrix, vehicle, constant.RIGHT)}
                count_up = {constant.UP: helper.count_empty_spots_in_dir(
                    matrix, vehicle, constant.UP)}
                count_down = {constant.DOWN: helper.count_empty_spots_in_dir(
                    matrix, vehicle, constant.DOWN)}
                self.slide(matrix, vehicle, count_left)
                self.slide(matrix, vehicle, count_right)
                self.slide(matrix, vehicle, count_up)
                self.slide(matrix, vehicle, count_down)
        return red

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
        if allowed and not helper.test_neighbour_empty(matrix, vehicle, direction):
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
            for count, data in enumerate(vehicle.position):
                matrix[vehicle.position[count]['y'],
                       vehicle.position[count]['x']] = 0
            for count, data in enumerate(vehicle.new_positions):
                matrix[vehicle.new_positions[count]['y'],
                       vehicle.new_positions[count]['x']] = vehicle.char

            vehicle.update_current_position()
