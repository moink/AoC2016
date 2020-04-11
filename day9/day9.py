import contextlib
import collections
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def run_part_1():
    data = advent_tools.read_whole_input()
    result = ''
    in_parentheses = False
    in_repeat_section = False
    to_repeat = ''
    repeat_inst = ''
    len_repeat = 0
    times_repeat = 0
    for char in data:
        if in_parentheses:
            if char == ')':
                len_repeat, times_repeat = (int(num) for num
                                            in repeat_inst.split('x'))
                in_parentheses = False
                in_repeat_section = True
                to_repeat = ''
            else:
                repeat_inst = repeat_inst + char
        elif in_repeat_section:
            to_repeat = to_repeat + char
            if len(to_repeat) == len_repeat:
                result = result + to_repeat * times_repeat
                in_repeat_section = False
        elif char == '(':
            in_parentheses = True
            repeat_inst = ''
        else:
            result = result + char
    print(len(result))

def get_uncomp_length(str):
    pass

def run_part_2():
    pass


if __name__ == '__main__':
    run_part_1()
    run_part_2()