"""
    Contains the Vehicle class for usage in solver.
"""
from rushhour import constant

class Vehicle:
    """
        Used for movement, holding positions, checking bounds
    """
    size = -1
    char = -1
    move_dir = ""
    move_count = 0
    mode = constant.MOVEMENT_DIRECTIONS[0]
    position = []  # depending on size 2 or 3 by 2 matrix
    new_positions = []

    def update_current_position(self):
        """
            Update to the new positions
        """
        count = 0
        for val in self.new_positions:
            self.position[count] = val
            count += 1

    def is_red_car(self):
        """
            Used for determining winning vehicle.
        """
        return self.char == 18

    def init_new_pos(self):
        """
            Intializes the new position so we always have the index ready with updated coordinates.
        """
        if self.size == 2:
            self.new_positions = [{'x': self.position[0]['x'], 'y': self.position[
                0]['y']}, {'x': self.position[1]['x'], 'y': self.position[1]['y']}]
        else:
            self.new_positions = [{'x': self.position[0]['x'], 'y': self.position[0]['y']},
                                  {'x': self.position[1]['x'], 'y': self.position[1]['y']},
                                  {'x': self.position[2]['x'], 'y': self.position[2]['y']}]

    def __str__(self):
        return str(self.char)

    # used for checking if in an explore state vehicle was already found
    def __eq__(self, other):
        return other is not None and self.char == other.char

    def __repr__(self):
        return str(self)
