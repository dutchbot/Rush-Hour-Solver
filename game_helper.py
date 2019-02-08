import constant
from vehicle_detector import VehicleDetector
from vehicle import Vehicle

def check_boundaries(number):
    """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
    if number < constant.BOARD_SIZE and number >= 0:
        return True
    return False

def determine_axis_by_direction(direction):
    if direction == constant.LEFT or direction == constant.RIGHT:
        return constant.MOVEMENT_DIRECTIONS[0]
    else:
        return constant.MOVEMENT_DIRECTIONS[1]

def find_vehicle_bounds(matrix, y_pos, x_pos, mode):
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