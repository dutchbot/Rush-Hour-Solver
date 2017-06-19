"""
    Contains vehicle detection classes.
"""

import helper

class VehicleDetector:
    """
        Abstract version
    """
    def find_vehicle(self, matrix, y_pos, x_pos, mode, vehicle, current):
        """
            Definition
        """
        pass

class VehicleDetector2(VehicleDetector):
    """
        Detects vehicles of size 2
    """
    def find_vehicle(self, matrix, y_pos, x_pos, mode, vehicle, current):
        """
            Find vehicles of size 2
        """
        if mode == 'hor':
            offset_hor = 1
            offset_ver = 0
            vehicle.mode = 'hor'
        else:
            offset_hor = 0
            offset_ver = 1
            vehicle.mode = 'ver'
        if helper.check_boundaries(y_pos + offset_ver) and \
            helper.check_boundaries(x_pos + offset_hor):
            if matrix[y_pos + offset_ver, x_pos + offset_hor] == current:  # size 2
                pos = [{'x': x_pos, 'y': y_pos}, {
                    'x': x_pos + offset_hor, 'y':  y_pos + offset_ver}]
                vehicle.position = pos
                vehicle.size = 2
                return vehicle
        return None

class VehicleDetector3(VehicleDetector):
    """
        Detects vehicles of size 3
    """
    def find_vehicle(self, matrix, y_pos, x_pos, mode, vehicle, current):
        """
            Find vehicles of size 3
        """
        if mode == 'hor':
            offset_hor = 2
            offset_ver = 0
            vehicle.mode = 'hor'
        else:
            offset_hor = 0
            offset_ver = 2
            vehicle.mode = 'ver'
        # size 3
        if helper.check_boundaries(y_pos + offset_ver) and \
            helper.check_boundaries(x_pos + offset_hor) and \
            matrix[y_pos + offset_ver, x_pos + offset_hor] == current:
            if mode == 'hor':  # ugly solution
                pos = [{'x': x_pos, 'y': y_pos}, {'x': x_pos + offset_hor - 1, 'y': y_pos +
                                          offset_ver}, {'x': x_pos + offset_hor, 'y':  y_pos + offset_ver}]
            else:
                pos = [{'x': x_pos, 'y': y_pos}, {'x': x_pos + offset_hor, 'y': y_pos +
                                          offset_ver - 1}, {'x': x_pos + offset_hor, 'y':  y_pos + offset_ver}]
            vehicle.position = pos
            vehicle.size = 3
            return vehicle
        elif helper.check_boundaries(y_pos - offset_ver) and \
            helper.check_boundaries(x_pos - offset_hor) and \
            matrix[y_pos - offset_ver, x_pos - offset_hor] == current:
            if mode == 'hor':  # ugly solution
                pos = [{'x': x_pos - offset_hor, 'y': y_pos - offset_ver}, {'x': x_pos - offset_hor + 1, 'y': y_pos -
                                                                    offset_ver}, {'x': x_pos, 'y':  y_pos}]
            else:
                pos = [{'x': x_pos - offset_hor, 'y': y_pos - offset_ver}, {'x': x_pos - offset_hor, 'y': y_pos -
                                                                    offset_ver + 1}, {'x': x_pos, 'y':  y_pos}]

            vehicle.position = pos
            vehicle.size = 3
            return vehicle

        else:
            if mode == 'hor':
                offset_hor = 1
                offset_ver = 0
                vehicle.mode = 'hor'
            else:
                offset_hor = 0
                offset_ver = 1
                vehicle.mode = 'ver'
            # size 3
            if helper.check_boundaries(y_pos - offset_ver) and \
                helper.check_boundaries(x_pos - offset_hor) and \
                helper.check_boundaries(y_pos + offset_ver) and \
                helper.check_boundaries(x_pos + offset_hor) and \
                matrix[y_pos - offset_ver, x_pos - offset_hor] == current and \
                matrix[y_pos + offset_ver, x_pos + offset_hor] == current:
                pos = [{'x': x_pos - offset_hor, 'y': y_pos - offset_ver},
                {'x': x_pos,'y': y_pos}, {'x': x_pos + offset_hor, 'y':  y_pos + offset_ver}]
                vehicle.position = pos
                vehicle.size = 3
                return vehicle
