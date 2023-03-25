import numpy as np
from random import randint, choice as randchoice
from tiles import MODULES, ALLOWED_MODULES, DIRECTION

"""
Written by Sathvik Kadaveru
3/19/2023
"""

# can't do more than 30x30
GRID_W = 20
GRID_H = 20


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


def get_adjacent_cells(cell, shape):
    """

    :param cell: The current cell
    :param shape: The shape of the grid
    :return: A list of adjacent cells
    """

    r, c = cell
    adjacent_cells = []
    if r > 0:
        adjacent_cells.append((r - 1, c))
    if r < shape[0] - 1:
        adjacent_cells.append((r + 1, c))
    if c > 0:
        adjacent_cells.append((r, c - 1))
    if c < shape[1] - 1:
        adjacent_cells.append((r, c + 1))
    return adjacent_cells


def get_valid_values_for_cell(cell, grid):
    """

    :param cell: The current cell
    :param grid: The current grid
    :return: valid values for current cell
    """
    r, c = cell
    shape = grid.shape
    valid = set(ALLOWED_MODULES.keys())
    for value in ALLOWED_MODULES:
        #
        top_value = grid[r - 1, c] if r > 0 else "═"
        if (
            top_value != "."
            and MODULES[top_value][DIRECTION.DOWN] != MODULES[value][DIRECTION.UP]
        ):
            valid.remove(value)
            continue
        #
        bottom_value = grid[r + 1, c] if r < shape[0] - 1 else "═"
        if (
            bottom_value != "."
            and MODULES[bottom_value][DIRECTION.UP] != MODULES[value][DIRECTION.DOWN]
        ):
            valid.remove(value)
            continue
        #
        left_value = grid[r, c - 1] if c > 0 else "║"
        if (
            left_value != "."
            and MODULES[left_value][DIRECTION.RIGHT] != MODULES[value][DIRECTION.LEFT]
        ):
            valid.remove(value)
            continue
        #
        right_value = grid[r, c + 1] if c < shape[1] - 1 else "║"
        if (
            right_value != "."
            and MODULES[right_value][DIRECTION.LEFT] != MODULES[value][DIRECTION.RIGHT]
        ):
            valid.remove(value)
            continue

    return list(valid)


def get_num_valid_for_adjacent_cells(cell, grid):
    """
    :param cell: the current cell
    :param grid: the current grid
    :return: The smallest number of valid values for one of the adjacent cells, a dict of cells with valid values
    """
    min_valid = 100000
    min_valid_cells = dict()
    # min_valid = the minimum value of valid values over all cells (ranges from 0 to 16)
    # min_valid_cells = those cells and their valid values
    for adj_cell in get_adjacent_cells(cell, grid.shape):
        r, c = adj_cell
        if grid[r, c] != ".":
            continue
        valid = get_valid_values_for_cell((r, c), grid)
        num_valid = len(valid)
        if num_valid == min_valid:
            min_valid_cells[(r, c)] = valid
        if num_valid < min_valid:
            min_valid = num_valid
            min_valid_cells = dict()
            min_valid_cells[(r, c)] = valid

    return min_valid, min_valid_cells


def wave_function_collapse(current_cell, grid):
    """
    Procedurally generates a grid
    :param current_cell:
    :param grid:
    :return:
    """
    while True:
        min_valid, min_valid_cells = get_num_valid_for_adjacent_cells(
            current_cell, grid
        )
        # there exists a cell with no valid options
        if min_valid == 0:
            return False

        # all adjacent cells are filled
        if min_valid >= 100000:
            return True

        random_cell = randchoice(list(min_valid_cells.keys()))
        random_value = randchoice(min_valid_cells[random_cell])
        grid[random_cell] = random_value

        # return if a failure is found
        if not wave_function_collapse(random_cell, grid):
            return False


def main():
    """
    The main method
    :return:
    """
    print("begin main")

    success = False
    while not success:
        grid = np.full((GRID_H, GRID_W), ".", dtype="U1")
        first_cell = (randint(0, GRID_H - 1), randint(0, GRID_W - 1))
        first_cell_value = randchoice(get_valid_values_for_cell(first_cell, grid))
        grid[first_cell] = first_cell_value

        success = wave_function_collapse(first_cell, grid)

    print_grid(grid)


if __name__ == "__main__":
    main()
