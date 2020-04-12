import contextlib
import collections
import copy
import functools
import itertools
import operator

import numpy as np
import pandas as pd
import re

import advent_tools

def get_position(dropped_time, disc_num, num_position, start_positions):
    real_time = dropped_time + disc_num
    return (start_positions + real_time) % num_position

def get_drop_time(lines):
    start_positions = []
    num_positions = []
    for line in lines:
        words = line.split()
        num_positions.append(int(words[3]))
        start_positions.append(int(words[-1][:-1]))
    for time in itertools.count():
        if all (get_position(time, i + 1, num_positions[i], start_positions[i])
                == 0
                for i in range(len(num_positions))):
            return time

def run_part_1():
    lines = advent_tools.read_input_lines()
    print(get_drop_time(lines))

def run_part_2():
    lines = advent_tools.read_input_lines()
    lines.append('Disc #7 has 11 positions; at time=0, it is at position 0.')
    print(get_drop_time(lines))

if __name__ == '__main__':
    run_part_1()
    run_part_2()