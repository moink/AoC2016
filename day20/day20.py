import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def find_all_outside():
    endpoints = pd.read_csv('input.txt', header=None, sep='-')
    endpoints.columns = ['start', 'end']
    endpoints.sort_values('start', inplace=True)
    endpoints.reset_index(inplace=True)
    high_end = endpoints.loc[0, 'end']
    result = []
    for row in endpoints.itertuples():
        if row.start > high_end + 1:
            result.append(high_end + 1)
            high_end = high_end + 1
        high_end = max(high_end, row.end)
    return result


def run_part_1():
    print(find_all_outside()[0])


def run_part_2():
    print(len(find_all_outside()))


if __name__ == '__main__':
    run_part_1()
    run_part_2()