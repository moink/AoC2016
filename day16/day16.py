import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def calc_checksum(start_data, needed_length):
    data = make_right_length(start_data, needed_length)
    while len(data) and len(data) % 2 == 0:
        print(len(data))
        new_data = ''
        for first, second in zip(data[0::2], data[1::2]):
            if first == second:
                new_data = new_data + '1'
            else:
                new_data = new_data + '0'
        data = new_data
    return data

def make_right_length(start_data, needed_length):
    data = start_data
    while len(data) < needed_length:
        rev = ''.join(['1' if a == '0' else '0' for a in reversed(data)])
        data = data + '0' + rev
    return data[:needed_length]


def run_part_1():
    print(calc_checksum('11110010111001001', 272))


def run_part_2():
    print(calc_checksum('11110010111001001', 35651584))


if __name__ == '__main__':
    run_part_1()
    run_part_2()