import contextlib
import collections
import copy
import functools
import itertools
from datetime import datetime

import numpy as np
import pandas as pd
import re

import advent_tools


class TrapGrid(advent_tools.PlottingGrid):

    def __init__(self, num_rows):
        num_cols = 100
        super().__init__((num_rows, num_cols))
        char_map = {'.': 0, '^': 1}
        self.read_input_file(char_map)
        for y_pos in range(0, num_rows - 1):
            shifted_right = np.pad(self.grid[y_pos, :-1], (1, 0))
            shifted_left = np.pad(self.grid[y_pos, 1:], (0, 1))
            self.grid[y_pos + 1] = shifted_left != shifted_right

    def count_safe(self):
        height, width = self.grid.shape
        return height * width - self.count()


def run_part_1():
    grid = TrapGrid(40)
    print(grid.count_safe())


def run_part_2():
    start_time = datetime.now()
    grid = TrapGrid(400000)
    print(grid.count_safe())
    elapsed_time = datetime.now() - start_time
    print(elapsed_time)


if __name__ == '__main__':
    run_part_1()
    run_part_2()