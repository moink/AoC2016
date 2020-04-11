import contextlib
import collections
import functools
import itertools

import advent_tools


def run_part_1():
    columns = [''] * 8
    lines = advent_tools.read_input_lines()
    result = []
    for line in lines:
        for pos, char in enumerate(line):
            columns[pos] = columns[pos] + char
    for col in columns:
        counter = collections.Counter(col)
        result.append(counter.most_common(1)[0][0])
    print(''.join(result))


def run_part_2():
    columns = [''] * 8
    lines = advent_tools.read_input_lines()
    result = []
    for line in lines:
        for pos, char in enumerate(line):
            columns[pos] = columns[pos] + char
    for col in columns:
        counter = collections.Counter(col)
        result.append(counter.most_common()[-1][0])
    print(''.join(result))


if __name__ == '__main__':
    # run_part_1()
    run_part_2()