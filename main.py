"""
    Main function to execute a default level or given level.
"""
from rushhour import constant
from rushhour import helper
from rushhour import node
from rushhour.solver import solver_bfs, solver_astar
from rushhour.data_dump import DataDump


def main(solver='bfs', text="....AA\n..BBCC\nrr..EF\nGGHHEF\n...IEF\n...IJJ"):
    """
        Runs the standard provided level
    """
    print(text)
    grid = helper.create_grid_from_text(text)
    start_matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
    if solver == 'bfs':
        solver = solver_bfs.SolverBfs()
        solver.solve(start_matrix)
    else:
        solution = "AA....\nBB..CC\n....rr\nGGHHEF\n...IEF\n.JJIEF"
        grid = helper.create_grid_from_text(solution)
        goal_matrix = helper.convert_to_matrix(grid, constant.BOARD_SIZE)
        start = node.Node(start_matrix)
        goal = node.Node(goal_matrix)
        solver = solver_astar.SolverAstar()
        solver.solve(start, goal)


def dump_data():
    """
        Dumps the matrices to ./data folder
    """
    local_data_dump = DataDump()
    local_data_dump.dump_data_to_file()


if __name__ == "__main__":
    main('bfs')
