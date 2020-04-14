import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt

import advent_tools

GOAL = 2

WALL = 1

EMPTY = 0

ROBOT = 3

class MazeState(advent_tools.StateForGraphs):

    def __init__(self, grid):
        self.grid = grid

    def init_from_file(self):
        lines = advent_tools.read_input_lines()
        char_map = {'.': EMPTY, '#': WALL, '0': ROBOT}
        for num in range(1, 10):
            char_map[str(num)] = GOAL
        for y_pos, line in enumerate(lines):
            for x_pos, char in enumerate(line):
                self.grid[y_pos, x_pos] = char_map[char]

    def __str__(self):
        return self.grid.tostring().decode('utf-16')

    def is_final(self):
        return not((self.grid == GOAL).any())

    def possible_next_states(self):
        y_rob, x_rob = np.argwhere(self.grid == ROBOT)[0]
        to_try = [(x_rob + 1, y_rob),
                  (x_rob - 1, y_rob),
                  (x_rob, y_rob + 1),
                  (x_rob, y_rob - 1)]
        result = set()
        for x_move, y_move in to_try:
            if self.grid[y_move, x_move] != WALL:
                new_grid = np.copy(self.grid)
                new_grid[y_rob, x_rob] = EMPTY
                new_grid[y_move, x_move] = ROBOT
                result.add(MazeState(new_grid))
        return result

    def show(self):
        """Show the grid in a new window

        Execution will be suspended until the window is closed

        Returns:
            None
        """
        plt.clf()
        plt.imshow(self.grid)
        plt.colorbar()
        plt.show()

class PartTwo(MazeState):

    def __init__(self, grid, start_pos=(0, 0)):
        super().__init__(grid)
        self.start_pos = start_pos

    def init_from_file(self):
        super().init_from_file()
        self.start_pos = np.argwhere(self.grid == ROBOT)[0]

    def is_final(self):
        if not super().is_final():
            return False
        robot_pos = np.argwhere(self.grid == ROBOT)[0]
        return (robot_pos == self.start_pos).all()

    def possible_next_states(self):
        y_rob, x_rob = np.argwhere(self.grid == ROBOT)[0]
        to_try = [(x_rob + 1, y_rob),
                  (x_rob - 1, y_rob),
                  (x_rob, y_rob + 1),
                  (x_rob, y_rob - 1)]
        result = set()
        for x_move, y_move in to_try:
            if self.grid[y_move, x_move] != WALL:
                new_grid = np.copy(self.grid)
                new_grid[y_rob, x_rob] = EMPTY
                new_grid[y_move, x_move] = ROBOT
                result.add(PartTwo(new_grid, self.start_pos))
        return result




def run_part_1():
    state = MazeState(np.zeros((37, 184)))
    state.init_from_file()
    print(advent_tools.number_of_bfs_steps(state))



def run_part_2():
    state = PartTwo(np.zeros((37, 184)))
    state.init_from_file()
    print(advent_tools.number_of_bfs_steps(state))


if __name__ == '__main__':
    # run_part_1()
    run_part_2()