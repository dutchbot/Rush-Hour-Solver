"""
    Contains static helper functions
"""
import constant

def check_boundaries(number):
    """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
    if number < constant.BOARD_SIZE and number >= 0:
        return True
    return False

def generate_hash(matrix):
    """
        Generate hash based on 2d array contents
    """
    return hash(matrix.tostring())
