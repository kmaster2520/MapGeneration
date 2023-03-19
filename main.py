import numpy as np
from random import randint, choice as randchoice
from tiles import MODULES, DIRECTION

"""
Written by Sathvik Kadaveru
3/19/2023
"""

# can't do more than 30x30
GRID_W = 30
GRID_H = 30


def print_grid(grid):
    shape = grid.shape
    for r in range(shape[0]):
        for c in range(shape[1]):
            print(grid[r][c], end=" ")
        print()


def get_adjacent_cells(cell, shape):
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
    r, c = cell
    shape = grid.shape
    valid = set(MODULES.keys())
    for value in MODULES:
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
    while True:
        min_valid, min_valid_cells = get_num_valid_for_adjacent_cells(
            current_cell, grid
        )
        if min_valid == 0:
            return  # we effed up
        if min_valid >= 100000:
            return  # all adjacent cells filled

        random_cell = randchoice(list(min_valid_cells.keys()))
        random_value = randchoice(min_valid_cells[random_cell])
        grid[random_cell] = random_value
        wave_function_collapse(random_cell, grid)


def main():
    print("begin main")

    grid = np.full((GRID_H, GRID_W), ".", dtype="U1")
    first_cell = (randint(0, GRID_H - 1), randint(0, GRID_W - 1))
    first_cell_value = randchoice(list(MODULES.keys()))
    grid[first_cell] = first_cell_value

    wave_function_collapse(first_cell, grid)

    print_grid(grid)


if __name__ == "__main__":
    main()
