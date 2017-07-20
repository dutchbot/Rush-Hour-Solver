"""
    Contains static helper functions
"""
import numpy
import rushhour.constant
from rushhour.vehicle_detector import VehicleDetector2, VehicleDetector3
from rushhour.vehicle import Vehicle


def check_boundaries(number):
    """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
    if number < rushhour.constant.BOARD_SIZE and number >= 0:
        return True
    return False


def generate_hash(matrix):
    """
        Generate hash based on 2d array contents
    """
    return hash(matrix.tostring())


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
    if rushhour.constant.DEBUG == 1:
        # TODO replace with logger
        print(matrix)
    return matrix


def check_valid_lane(matrix, y_pos, x_pos, count_empty, move_dir):
    """
        Boundary check and if spot is empty
    """
    y_pos = y_pos + move_dir['offset_ver'] * count_empty
    x_pos = x_pos + move_dir['offset_hor'] * count_empty
    return check_boundaries(y_pos) and \
        check_boundaries(x_pos) and \
        matrix[y_pos, x_pos] == 0


def check_valid_move(matrix, vehicle, move_dir):
    """
        Check if move falls within boundaries and if spot is empty
    """
    # print(move_dir)
    y_pos = vehicle.position[move_dir['index']]['y'] + move_dir['offset_ver']
    x_pos = vehicle.position[move_dir['index']]['x'] + move_dir['offset_hor']
    return check_boundaries(y_pos) and \
        check_boundaries(x_pos) and \
        matrix[y_pos][x_pos] == 0

    # look at object boundaries/size


def test_neighbour_empty(matrix, vehicle, direction):
    """
        Look if next position relative to vehicle size is empty spot
    """
    move_dir = get_move_dir(vehicle, direction)
    return check_valid_move(matrix, vehicle, move_dir)


def get_move_dir(vehicle, direction):
    """
        Determine the correct index and offset for use in movement and test_empty functions.
    """
    move_dir = {'index': 0, 'offset_ver': 0, 'offset_hor': 0}
    if direction == rushhour.constant.LEFT:
        move_dir['offset_hor'] = -1
    elif direction == rushhour.constant.RIGHT:
        move_dir['offset_hor'] = 1
        if vehicle.size == 2:
            move_dir['index'] = 1
        else:
            move_dir['index'] = 2
    elif direction == rushhour.constant.UP:
        move_dir['offset_ver'] = -1
    elif direction == rushhour.constant.DOWN:
        move_dir['offset_ver'] = 1
        if vehicle.size == 2:
            move_dir['index'] = 1
        else:
            move_dir['index'] = 2

    return move_dir


def count_empty_spots_in_dir(matrix, vehicle, direction):
    """
        When count_empty is incremented the position values increment or decrement,
        according to direction and horizontal/vertical mode.
        Thus deriving the empty spots in a given direction.
    """
    count_empty = 1  # in order for multiplier to work
    move_dir = get_move_dir(vehicle, direction)
    x_pos = vehicle.position[move_dir['index']]['x']
    y_pos = vehicle.position[move_dir['index']]['y']

    while check_valid_lane(matrix, y_pos, x_pos, count_empty, move_dir):
        count_empty += 1
    if count_empty == 1:
        return 0
    return count_empty - 1


def try_to_find_vehicle(matrix, y_pos, x_pos):
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


def try_to_find_vehicle_c(matrix, step):
    """
        Find vehicles either horizontal or vertical, both is not possible at the same position.
    """
    for y_pos, row in enumerate(matrix):
        for x_pos, column in enumerate(row):
            dirc = step['direction']
            if dirc == rushhour.constant.LEFT or dirc == rushhour.constant.RIGHT:
                vehicle = find_vehicle_bounds(
                    matrix, y_pos, x_pos, 'hor')
            else:
                vehicle = find_vehicle_bounds(
                    matrix, y_pos, x_pos, 'ver')

            if vehicle and vehicle.char == step['char']:
                return vehicle
    return None


def find_vehicle_bounds(matrix, y_pos, x_pos, mode):
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
                {'char': rushhour.constant.LABEL[position], 'y': county, 'x': countx})
            countx += 1
        county += 1

    if rushhour.constant.DEBUG == 1:
        # TODO replace with logger
        print(len(indexes))

    return indexes
