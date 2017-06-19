"""
    Main function to execute a default level or given level.
"""

from solver import Solver
import constant

def main(text="....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"):
    """
        Runs the standard provided level
    """
    print(text)
    solver = Solver()
    grid = solver.create_grid_from_text(text)
    matrix = solver.convert_to_matrix(grid, constant.BOARD_SIZE)
    solver.solve(matrix)

main()
