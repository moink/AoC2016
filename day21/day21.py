import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

def rotate(l, n):
    n = n % len(l)
    return l[n:] + l[:n]


def run_program(instructions, password):
    pwd = list(password)
    for line in instructions:
        words = line.split()
        operation = words[0] + ' ' + words[1]
        if operation == 'swap position':
            pos1 = int(words[2])
            pos2 = int(words[-1])
            pwd[pos1], pwd[pos2] = pwd[pos2], pwd[pos1]
        elif operation == 'swap letter':
            pos1 = pwd.index(words[2])
            pos2 = pwd.index(words[-1])
            pwd[pos1], pwd[pos2] = pwd[pos2], pwd[pos1]
        elif operation == 'rotate left':
            amount = int(words[2])
            pwd = rotate(pwd, amount)
        elif operation == 'rotate right':
            amount = int(words[2])
            pwd = rotate(pwd, -amount)
        elif operation == 'rotate based':
            index = pwd.index(words[-1])
            if index >= 4:
                amount = index + 2
            else:
                amount = index + 1
            pwd = rotate(pwd, -amount)
        elif operation == 'reverse positions':
            start = int(words[2])
            end = int(words[-1])
            pwd[start:end + 1] = reversed(pwd[start:end + 1])
        elif operation == 'move position':
            old_spot = int(words[2])
            new_spot = int(words[-1])
            pwd.insert(new_spot, pwd.pop(old_spot))
    return (''.join(pwd))


def find_input(scrambled):
    instructions = advent_tools.read_input_lines()
    for permut in itertools.permutations(list(scrambled)):
        result = run_program(instructions, permut)
        if result == scrambled:
            return ''.join(permut)

def run_part_1():
    instructions = advent_tools.read_input_lines()
    password = 'abcdefgh'
    print(run_program(instructions, password))


def run_part_2():
    print(find_input('fbgdceah'))


if __name__ == '__main__':
    run_part_1()
    run_part_2()