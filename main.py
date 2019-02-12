"""
    Main function to execute a default level or given level.
"""
import constant
import helper
#from solver import Solver
import rush_hour
from data_dump import DataDump
import bfs, dfs
import argparse

def main():
    """ Commands and descriptions """
    parser = argparse.ArgumentParser(
        description='Solve rush hour levels with bfs and dfs approach. Or execute pre defined levels with steps to solution in order to generate board data. ')
    parser.add_argument('--solve', action="store_true",
                        default=True, dest="mode", help='Solve a level bfs or dfs.')
    parser.add_argument('--generate', action="store_false",
                    default=True, dest="mode", help='Generate board data for levels.txt.')
    args = parser.parse_args()

    if args.mode:
        solve()
    else:
        generate_board_data()

    input("Press Enter to continue...")


def solve(text="....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"):
    """
        Runs the standard provided level
    """
    text = "AAOBCC\n..OB..\nrrO...\nDEEFFP\nD..K.P\nHH.K.P"
    print(text)
    game = rush_hour.RushHour()
    solver_dfs = dfs.SolverDfs(game)
    solver_bfs = bfs.SolverBfs()
    grid = helper.create_matrix_from_text(text)
    matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
    print(matrix)
    print("Running depth-first search..")
    solver_dfs.solve(matrix)
    print("Running breadth-first search..")
    solver_bfs.solve(matrix)

def generate_board_data():
    """
        Dumps the matrices to ./data folder
    """
    local_data_dump = DataDump()
    local_data_dump.dump_data_to_file()

if __name__ == "__main__":
    main()
