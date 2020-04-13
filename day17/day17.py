import contextlib
import collections
import copy
import functools
import hashlib
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

class MazePath(advent_tools.StateForGraphs):

    def __init__(self, path, position):
        self.path = path
        self.position = position

    def __str__(self):
        return self.path

    def is_final(self):
        return self.position == (3, 3)

    def possible_next_states(self):
        results = set()
        x, y = self.position
        directions = {'U': (x, y - 1), 'D': (x, y + 1),
                      'L': (x - 1, y), 'R': (x + 1, y)}
        hashed = hashlib.md5(self.path.encode('utf-8')).hexdigest()
        open_doors = 'bcdef'
        for door, (direction, (new_x, new_y)) in zip(hashed[:4],
                                                     directions.items()):
            if (0 <= new_x <=3) and (0 <= new_y <=3) and door in open_doors:
                results.add(MazePath(self.path + direction, (new_x, new_y)))
        return results


def run_part_1():
    # passcode = 'hhhxzeay'
    passcode = 'hhhxzeay'
    initial_state = MazePath(passcode, (0, 0))
    print(str(advent_tools.find_final_state(initial_state))[len(passcode):])


def run_part_2():
    passcode = 'hhhxzeay'
    initial_state = MazePath(passcode, (0, 0))
    print(advent_tools.longest_path(initial_state))


if __name__ == '__main__':
    run_part_1()
    run_part_2()