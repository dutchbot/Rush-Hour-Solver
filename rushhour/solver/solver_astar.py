"""
    Contains the neccesary (helper) functions to solve the rush hour game. (hardcoded to 6x6)
    In a bruteforce manner, BFS approach.
"""
import copy
from rushhour import node
from rushhour import helper
from rushhour import constant


class SolverAstar:
    """
        problem here is each node will represent a matrix state that is found, but how will we assign its score?
        Simply checking if the red car is moved is not enough i think?

        its a 2d non-linear problem so score decrement per node wont work properly.
    """

    def __init__(self):
        self.closed_set = []
        self.open_set = []  # this starts with the start_matrix node..
        """
        We need a node class:
        matrix data
        hash
        from
        to
        """
        self.came_from = {}
        self.fscore = {}  # the total cost per node of start to goal struct hash->score
        self.gscore = {}  # the cost of reaching a certain node hash->score
        #self.predecessor = {}
        self.total_steps = 0
        self.output = True
        self.base_cost = 90
        self.countertje = 0

    def propose(self, current, neighbour):
        """
            Add new hashed matrix to predeccesor dictionary if not exists,
            and add to queue for next exploration.
        """
        if not neighbour.sts() in self.came_from:
            self.came_from[neighbour.sts()] = current
            # need to copy it because python references by default.
            self.open_set.append(neighbour)
            return True
        return False

    def solve(self, start, goal):
        """
            Keep exploring unseen states until red vehicle is found at destination.
        """
        solved = False
        #elf.propose(start, None)
        self.open_set.append(start)
        print(start)
        self.gscore[start.sts()] = 0
        self.fscore[start.sts()] = self.estimate_cost(start, goal)
        count = 0
        red = None
        while self.open_set:
            current = self.open_set.pop()  # take a new matrix from the queue
            self.closed_set.append(current)

            red = self.explore(current)

            if red != None and helper.is_win_position(red) and not solved:
                print("Found solution in " + str(count) + " nodes/states!")
                print(current.get_matrix())
                print(goal.get_matrix())
                solved = True
                break
            count += 1

            for neighbor in current.get_neighbours():  # we should have four neighbours?
                if neighbor in self.closed_set:
                    continue

                if neighbor not in self.open_set:
                    self.open_set.append(neighbor)

                tentative_gscore = self.gscore[current.sts(
                )] + self.dist_between(current, neighbor)
                # print(tentative_gscore)
                if tentative_gscore >= self.gscore[neighbor.sts()]:
                    print("skip")
                    continue  # This is not a better path.

                # This path is the best until now. Record it!
                # equivalent of our predecessor
                self.came_from[neighbor.sts()] = current
                self.gscore[neighbor.sts()] = tentative_gscore
                self.fscore[neighbor.sts()] = self.gscore[neighbor.sts()] + \
                    self.estimate_cost(neighbor, goal)

    def estimate_cost(self, start, goal):
        """
         based on number of vertical or horizontal vehicels?
        """
        print("90, for now")
        if start.has_rr_moved():
            self.base_cost -= 1
            return self.base_cost
        # if goal.
        return 90

    def dist_between(self, current, neighbour):
        # print(current.get_neighbours())
        return current.get_neighbours().index(neighbour)

# this should stay the same i guess
    def explore(self, current):
        """
            Scan the entire matrix per point for vehicles,
            making sure that each vehicle is moved only once per exploration.
        """
        red = None
        seen_vehicles = []
        matrix = current.get_matrix()
        for y_pos, row in enumerate(matrix):
            for x_pos, column in enumerate(row):
                unseen, vehicle = self.is_unseen_vehicle(
                    matrix, y_pos, x_pos, seen_vehicles)
                if not unseen:
                    continue
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
                self.slide(current, vehicle, count_left)
                self.slide(current, vehicle, count_right)
                self.slide(current, vehicle, count_up)
                self.slide(current, vehicle, count_down)
        return red

    def is_unseen_vehicle(self, matrix, y_pos, x_pos, vehicles):
        vehicle = helper.try_to_find_vehicle(matrix, y_pos, x_pos)
        duplicate = False
        for comp_vehicle in vehicles:
            if vehicle is None:
                break
            if comp_vehicle == vehicle:
                duplicate = True
                break
        if not vehicle or duplicate:  # skip the same vehicle
            return False, None
        vehicles.append(vehicle)
        return True, vehicle

    def slide(self, current, vehicle, direction):
        """
            Derive the axis from the direction and determine of stepsize is negative or positive
        """
        new_matrix = copy.copy(current.get_matrix()
                               )  # copy in order to generate correct hash
        neighbour = node.Node(new_matrix)
        dir_key = list(direction.keys())[0]
        stepsize = direction[dir_key]
        test = {constant.UP: 'y', constant.DOWN: 'y',
                constant.LEFT: 'x', constant.RIGHT: 'x'}
        if dir_key == constant.LEFT or dir_key == constant.UP:
            stepsize = -stepsize
        return self.slider(current, neighbour, vehicle, dir_key, test[dir_key], stepsize)
        # apply as neighbour to current node?
        # val = self.propose(current,neighbour)

    def slider(self, current, neighbour, vehicle, direction, plc, stepsize):
        """
            Slide on empty spots depending on vehicle size and direction
        """
        vehicle.init_new_pos()
        matrix = neighbour.get_matrix()
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

            self.update_matrix(neighbour, vehicle)  # THIS CALCS HASH ANEW

            if vehicle.is_red_car():
                neighbour.rr_moved += 1
            self.countertje += 1
            # print("added nieghbour" + str(self.countertje)) # le 36|?
            current.add_neighbour(neighbour)
            self.gscore[neighbour.sts()] = 0  # cost increases
            # print(self.gscore)

            return True
        return False

    def update_matrix(self, neighbor, vehicle):
        """
            Update the matrix with new vehicle positions, and update vehicle to the new position
        """
        matrix = neighbor.get_matrix()
        if vehicle.new_positions:
            for count, data in enumerate(vehicle.position):
                matrix[vehicle.position[count]['y'],
                       vehicle.position[count]['x']] = 0
            for count, data in enumerate(vehicle.new_positions):
                matrix[vehicle.new_positions[count]['y'],
                       vehicle.new_positions[count]['x']] = vehicle.char

            vehicle.update_current_position()
            neighbor.update_hash()
