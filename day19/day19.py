import contextlib
import collections
import copy
import functools
import itertools
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import re

import advent_tools


def steal_from_left(num_elves):
    elves = list(range(1, num_elves + 1))
    i = 0
    while elves[-1] != elves[-2]:
        elves.append(elves[i])
        i = i + 2
    return elves[-1]

def steal_from_across(num_elves):
    first_steal = num_elves // 2 + 1
    before = collections.deque(range(1, first_steal))
    after = collections.deque(range(first_steal + 1, num_elves + 1))
    while after:
        after.append(before.popleft())
        before.append(after.popleft())
        if len(before) > len(after):
            before.pop()
        else:
            after.popleft()
    return before[0]

def run_part_1():
    print(steal_from_left(3018458))


def run_part_2():
    print(steal_from_across(3018458))


if __name__ == '__main__':
    # run_part_1()
    run_part_2()