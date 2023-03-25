import numpy as np
from random import randint, choice as randchoice

from util import get_cell_adjacency, has_valid_connection
from setup import generate_modules, display_grid

"""
Written by Sathvik Kadaveru
3/25/2023
"""

# can't do more than 30x30
GRID_W = 25
GRID_H = 25

MODULE_LIST = []


def print_grid(grid):
    """
    Prints the grid
    :param grid: The current grid
    :return:
    """
    shape = grid.shape
    for r in range(shape[0]):
        for c in range(shape[1]):
            print(grid[r][c], end=" ")
        print()


def get_valid_values_for_cell(cell, grid):
    """
    Precondition: this cell does not have a value

    :param cell: The current cell
    :param grid: The current grid
    :return: valid (integer index) values for current cell
    """
    valid = []

    adjacency = get_cell_adjacency(cell, grid.shape)

    # iterate through all allowed modules
    for i, module in enumerate(MODULE_LIST):
        still_valid = True

        # check if this module is compatible with adjacent cell modules
        for direction, adj_cell in adjacency.items():
            # ignore if adjacent cell has no value
            if grid[adj_cell] < 0:
                continue

            adj_cell_module = MODULE_LIST[grid[adj_cell]]
            # break if valid connection does not exist with even one adjacent cell
            if not has_valid_connection(module, adj_cell_module, direction):
                still_valid = False
                break

        if still_valid:
            valid.append(i)

    return valid


def get_valid_values_for_adjacent_cells(cell, grid):
    adjacency = get_cell_adjacency(cell, grid.shape)
    valid_values_map = dict()
    for direction, adj_cell in adjacency.items():
        if grid[adj_cell] >= 0:
            continue
        valid_values_map[adj_cell] = get_valid_values_for_cell(adj_cell, grid)
    return valid_values_map


def wave_function_collapse(current_cell, grid):
    """
    Procedurally generates a grid
    Precondition: current_cell has a value
    :param current_cell:
    :param grid:
    :return:
    """
    while True:
        valid_values_map = get_valid_values_for_adjacent_cells(current_cell, grid)

        lowest_entropy = 1000000
        best_cell = None
        for adj_cell, valid_values in valid_values_map.items():
            num_valid_values = len(valid_values)
            if num_valid_values < lowest_entropy:
                lowest_entropy = num_valid_values
                best_cell = adj_cell

        if lowest_entropy == 0:
            return False # messed up, need to restart

        if best_cell is None:
            return True  # all adjacent cells filled

        grid[best_cell] = randchoice(get_valid_values_for_cell(best_cell, grid))
        if not wave_function_collapse(best_cell, grid):
            return False


def main():
    global MODULE_LIST
    MODULE_LIST, tile_w, tile_h = generate_modules("pipes")
    # print(MODULE_LIST)

    success = False
    iteration_number = 1
    while not success:
        grid = np.full((GRID_H, GRID_W), -1, np.int32)
        first_cell = (randint(0, GRID_H - 1), randint(0, GRID_W - 1))
        grid[first_cell] = randchoice(get_valid_values_for_cell(first_cell, grid))
        # print(grid[first_cell])

        iteration_number += 1
        success = wave_function_collapse(first_cell, grid)

    print_grid(grid)
    print(f"Attempt Number: {iteration_number}")

    display_grid(grid, MODULE_LIST, tile_w, tile_h)


if __name__ == '__main__':
    main()
