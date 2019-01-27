"""
    Main function to execute a default level or given level.
"""
import constant
import helper
from solver import Solver
from data_dump import DataDump

def main(text="....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"):
    """
        Runs the standard provided level
    """
    print(text)
    solver = Solver()
    grid = helper.create_grid_from_text(text)
    matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
    solver.solve(matrix)
    input("Press Enter to continue...")

def dump_data():
    """
        Dumps the matrices to ./data folder
    """
    local_data_dump = DataDump()
    local_data_dump.dump_data_to_file()

if __name__ == "__main__":
    main()
