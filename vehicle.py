"""
    Contains the Vehicle class for usage in solver.
"""
import constant
import helper

class Vehicle:
    """
        Used for movement, holding positions, checking bounds
    """
    size = -1
    identifier = -1
    has_moved = False
    mode = constant.MOVEMENT_DIRECTIONS[0]
    position = []  # depending on size 2 or 3 by 2 matrix

    def drive(self, axis, stepsize):
        current_hash =  helper.generate_hash(str(self.position))
        self.position[0][axis] += stepsize
        self.position[1][axis] += stepsize
        if self.size == 3:
            self.position[2][axis] += stepsize
        after_hash = helper.generate_hash(str(self.position))
        if(current_hash != after_hash):
            self.has_moved = True

    def reset_has_moved(self):
        self.has_moved = False

    def is_red_car(self):
        """
            Used for determining winning vehicle.
        """
        return self.identifier == 18

    def __str__(self):
        return str(self.identifier)

    # used for checking if in an explore state vehicle was already found
    def __eq__(self, other):
        return other is not None and self.identifier == other.identifier

    def __repr__(self):
        return str(self)
