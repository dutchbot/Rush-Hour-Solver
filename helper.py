"""
    Contains static helper functions
"""
import constant
import numpy
import copy
from vehicle_detector import VehicleDetector2, VehicleDetector3
from vehicle import Vehicle

def check_boundaries(number):
    """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
    if number < constant.BOARD_SIZE and number >= 0:
        return True
    return False

def generate_hash(value):
    """
        Generate hash based on string
    """
    return hash(value)

def is_win_position(vehicle):
    """
        Checks for the static size coordinates and correct character.
    """
    if vehicle.is_red_car() and vehicle.position[0]['x'] == 4 and vehicle.position[1]['x'] == 5:
        return True
    return False

def convert_to_matrix(grid, size):
    """
        Convert text string to numerical matrix
    """
    matrix = numpy.zeros(shape=(size, size))
    for position in grid:
        matrix[position['y'], position['x']] = position['char']
    if constant.DEBUG == 1:
        print(matrix)
    return matrix

def check_valid_lane(matrix, y, x, offset_ver, offset_hor):
    """
        Boundary check and if spot is empty
    """
    y_pos = y + offset_ver
    x_pos = x + offset_hor
    return check_boundaries(y_pos) and \
        check_boundaries(x_pos) and \
        matrix[y_pos, x_pos] == 0

def check_valid_move(matrix, vehicle, index, offset, offset_hor):
    """
        Check if move falls within boundaries and if spot is empty
    """
    y_pos = vehicle.position[index]['y'] + offset
    x_pos = vehicle.position[index]['x'] + offset_hor
    return check_boundaries(y_pos) and \
        check_boundaries(x_pos) and \
        matrix[y_pos][x_pos] == 0

    # look at object boundaries/size
def is_board_position_empty_in_direction(matrix, vehicle, direction):
    """
        Look if next position relative to vehicle size is empty spot
    """
    if direction == constant.LEFT:
        return check_valid_move(matrix, vehicle, 0, 0, -1)
    elif direction == constant.RIGHT:
        if vehicle.size == 2:
            return check_valid_move(matrix, vehicle, 1, 0, 1)
        else:
            return check_valid_move(matrix, vehicle, 2, 0, 1)
    elif direction == constant.UP:
        return check_valid_move(matrix, vehicle, 0, -1, 0)
    elif direction == constant.DOWN:
        if vehicle.size == 2:
            return check_valid_move(matrix, vehicle, 1, 1, 0)
        else:
            return check_valid_move(matrix, vehicle, 2, 1, 0)

    return False

def count_empty_spots_in_dir(matrix, vehicle, direction):
    """
        When count_empty is incremented the position values increment or decrement,
        according to direction and horizontal/vertical mode.
        Thus deriving the empty spots in a given direction.
    """
    count_empty = 1  # in order for multiplier to work
    x_pos = vehicle.position[0]['x']
    y_pos = vehicle.position[0]['y']
    indexed_size = vehicle.size - 1
    if direction == constant.LEFT:
        offset_hor = -1
        offset_ver = 0
    elif direction == constant.RIGHT:
        x_pos = vehicle.position[indexed_size]['x']
        y_pos = vehicle.position[indexed_size]['y']
        offset_hor = 1
        offset_ver = 0
    elif direction == constant.UP:
        offset_hor = 0
        offset_ver = -1
    elif direction == constant.DOWN:
        x_pos = vehicle.position[indexed_size]['x']
        y_pos = vehicle.position[indexed_size]['y']
        offset_hor = 0
        offset_ver = 1

    while check_valid_lane(matrix, y_pos, x_pos, offset_ver * count_empty, offset_hor * count_empty):
        count_empty += 1
    if count_empty == 1:
        return 0
    else:
        return count_empty - 1

def traverse_optimal_moves(predecessors, end_board):
    board_hash = predecessors[generate_hash(end_board.tostring())]
    count = 0
    while board_hash != None:
        count += 1
        #print(self.list_visited_boards[board_hash])
        board_hash = predecessors[board_hash]
    print("Graph consisted of " + str(count) + " steps!")


def propose(predecessors, list_visited_boards,current_board, prev_board, working_set):
    """ 
        Add new hashed matrix to predeccesor dictionary if not exists,
        and add to queue or stack for next exploration.
    """
    if not generate_hash(current_board.tostring()) in predecessors:
        if prev_board is not None:
            prev_board = generate_hash(prev_board.tostring())
        predecessors[generate_hash(current_board.tostring())] = prev_board
        # need to copy it because python references by default.
        list_visited_boards[generate_hash(current_board.tostring())] = copy.deepcopy(current_board)
        working_set.append(copy.deepcopy(current_board))
        return True
    return False

def find_vehicle_on_board_position(matrix, y_pos, x_pos):
    """
        Find vehicles either horizontal or vertical, both is not possible at the same position.
    """
    if matrix[y_pos, x_pos] != 0:
        hor_vehicle = find_vehicle_bounds(matrix, y_pos, x_pos, 'hor')
        ver_vehicle = find_vehicle_bounds(matrix, y_pos, x_pos, 'ver')
        if ver_vehicle:
            return ver_vehicle
        if hor_vehicle:
            return hor_vehicle

def determine_axis_by_direction(direction):
    if direction == constant.LEFT or direction == constant.RIGHT:
        return constant.MOVEMENT_DIRECTIONS[0]
    else:
        return constant.MOVEMENT_DIRECTIONS[1]

def find_vehicle_axis(matrix, step):
    """
        Find vehicles either horizontal or vertical, both is not possible at the same position.

        This function will probably become obsolete when we move on the grid by vehicle only (OOP)
    """
    for y_pos, row in enumerate(matrix):
        for x_pos, column in enumerate(row):
            axis = determine_axis_by_direction(step['direction'])
            vehicle = find_vehicle_bounds(matrix, y_pos, x_pos, axis)
            if vehicle and vehicle.identifier == step['char']:
                return vehicle
    return None

def find_vehicle_bounds(matrix, y_pos, x_pos, mode):
    """
        Detect the start and end point of vehicles depending on size,
        we can either have a size of 2 or 3 at a given spot not both.
    """
    vehicle_identifier = matrix[y_pos, x_pos]
    vehicle = Vehicle()
    vehicle.identifier = vehicle_identifier
    if vehicle_identifier != 0:
        size_3 = VehicleDetector3().find_vehicle(
            matrix, y_pos, x_pos, mode, vehicle, vehicle_identifier)
        if size_3:
            return size_3
        size_2 = VehicleDetector2().find_vehicle(
            matrix, y_pos, x_pos, mode, vehicle, vehicle_identifier)
        if size_2:
            return size_2
    return None

def create_grid_from_text(text, file=False):
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
