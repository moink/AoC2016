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

def get_uncomp_length(compressed):
    if compressed.startswith('('):
        instruction, after_inst = compressed.split(')', maxsplit=1)
        len_repeat, times_repeat = (int(num) for num
                                    in instruction[1:].split('x'))
        to_repeat = after_inst[:len_repeat]
        rest = after_inst[len_repeat:]
        return (times_repeat * get_uncomp_length(to_repeat)
                + get_uncomp_length(rest))
    elif '(' in compressed:
        before_paren, after_paren = compressed.split('(', maxsplit=1)
        return (get_uncomp_length(before_paren)
                + get_uncomp_length('(' + after_paren))
    else:
        return len(compressed)

def run_part_2():
    print(get_uncomp_length(advent_tools.read_whole_input()))


if __name__ == '__main__':
    run_part_1()
    run_part_2()