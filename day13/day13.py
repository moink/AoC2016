import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def is_wall(x, y):
    if x < 0 or y < 0:
        return True
    poly = x * x + 3 * x + 2 * x * y + y + y * y + 1364
    binary = bin(poly)[2:]
    num_ones = sum(int(digit) for digit in binary)
    if num_ones % 2 == 1:
        return True
    return False


class MazeLocation(advent_tools.StateForGraphs):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x},{self.y}'

    def possible_next_states(self):
        result = set()
        x = self.x
        y = self.y
        adjacent = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for point in adjacent:
            if not(is_wall(*point)):
                result.add(MazeLocation(*point))
        return result


    def is_final(self):
        return self.x == 31 and self.y == 39


def run_part_1():
    initial_state = MazeLocation(1, 1)
    print(advent_tools.number_of_bfs_steps(initial_state))


def run_part_2():
    initial_state = MazeLocation(1, 1)
    print(advent_tools.number_of_reachable_in_steps(initial_state, 50))

if __name__ == '__main__':
    run_part_1()
    run_part_2()