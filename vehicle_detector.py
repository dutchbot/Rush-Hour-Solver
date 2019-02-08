"""
    Contains vehicle detection classes.

    This is not generic enough.
"""

import game_helper

class VehicleDetector:
    """
        Detects vehicles
    """
    def find_vehicle(self, matrix, y_pos, x_pos, mode, vehicle, current):
        """
            Find vehicles of max_size 3
        """
        pos = []
        max_size = 3
        for offset in range(0, max_size):
            if mode == 'hor' and game_helper.check_boundaries(x_pos + offset) and matrix[y_pos, x_pos + offset] == current:
                pos.append({'x': x_pos + offset, 'y': y_pos}) 
            elif mode == 'ver' and game_helper.check_boundaries(y_pos + offset) and matrix[y_pos + offset, x_pos] == current:
                pos.append({'x': x_pos, 'y': y_pos + offset})

        if pos.__len__() == 2 or pos.__len__() == 3:
            vehicle.position = pos
            vehicle.size = pos.__len__()
            vehicle.mode = mode
            return vehicle
        
        return None