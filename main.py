import numpy as np
from random import randint, choices as randchoice
import argparse

from util import get_cell_adjacency, has_valid_connection
from setup import generate_modules, display_grid, DEFAULT_WEIGHT

"""
Written by Sathvik Kadaveru
3/25/2023
"""

# can't do more than 30x30
GRID_W = 60
GRID_H = 40

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


def wave_function_collapse(grid):
    """
    Procedurally generates a grid
    Precondition: current_cell has a value
    :param current_cell:
    :param grid:
    :return:
    """

    first_cell = (randint(0, GRID_H - 1), randint(0, GRID_W - 1))
    grid[first_cell] = randchoice(get_valid_values_for_cell(first_cell, grid))[0]
    cell_stack = [first_cell]
    while len(cell_stack) > 0:
        current_cell = cell_stack[-1]

        valid_values_map = get_valid_values_for_adjacent_cells(current_cell, grid)
        lowest_entropy = 1000000
        best_cell = None
        valid_choices_for_best_cell = []
        for adj_cell, valid_values in valid_values_map.items():
            num_valid_values = len(valid_values)
            if num_valid_values < lowest_entropy:
                lowest_entropy = num_valid_values
                best_cell = adj_cell
                valid_choices_for_best_cell = valid_values

        if lowest_entropy == 0:
            return False  # messed up, need to restart

        if best_cell is None:
            cell_stack.pop()
            continue  # all adjacent cells filled

        weights = [MODULE_LIST[i].get("weight", DEFAULT_WEIGHT) for i in valid_choices_for_best_cell]
        grid[best_cell] = randchoice(valid_choices_for_best_cell, weights=weights)[0]
        cell_stack.append(best_cell)

    return True

def main():
    global MODULE_LIST

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="name of pattern to run", default="pipes")
    parser.add_argument("-c", "--config", help="name of config to run", default=None)
    parser.add_argument("--grid", help="show grid lines in image", action="store_true")
    parser.add_argument("--save", help="save image", action="store_true")
    parser.add_argument("--animate", help="animate", action="store_true")
    args = parser.parse_args()
    print(args)

    MODULE_LIST, tile_w, tile_h = generate_modules(args.name, config=args.config)
    # print(MODULE_LIST)

    success = False
    iteration_number = 0
    grid = np.full((GRID_H, GRID_W), -1, np.int32)
    while not success:
        grid = np.full((GRID_H, GRID_W), -1, np.int32)
        iteration_number += 1
        success = wave_function_collapse(grid)

        if iteration_number > 30:
            print('no can do')
            break

    # print_grid(grid)
    print(f"Attempt Number: {iteration_number}")

    display_grid(grid, MODULE_LIST, (tile_w, tile_h), showGrid=args.grid, saveGrid=args.save)


if __name__ == '__main__':
    main()
