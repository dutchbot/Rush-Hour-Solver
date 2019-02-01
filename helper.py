"""
    Contains static helper functions
"""
import constant
import numpy
import copy

def generate_hash(value):
    """
        Generate hash based on string
    """
    return hash(value)

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

def create_matrix_from_text(text, file=False):
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

def check_boundaries(number):
    """ Checks if number falls within 0 and default(constant.BOARD_SIZE)"""
    if number < constant.BOARD_SIZE and number >= 0:
        return True
    return False
