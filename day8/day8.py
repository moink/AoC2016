import contextlib
import collections
import functools
import itertools
import re

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import advent_tools


class LittleScreen(advent_tools.PlottingGrid):

    def illuminate_rectangle(self, rows, cols):
        self.grid[0:rows, 0:cols] = 1

    def rotate_row(self, row, amount):
        self.grid[row, :] = np.roll(self.grid[row, :], amount)

    def rotate_col(self, col, amount):
        self.grid[:, col] = np.roll(self.grid[:, col], amount)

    def run_instruction(self, full_instruction):
        words = full_instruction.split()
        instruction = words[0]
        if instruction == 'rect':
            cols, rows = (int(num) for num in words[1].split('x'))
            self.illuminate_rectangle(rows, cols)
        else: # instruction == 'rotate':
            axis = words[1]
            index = int(words[2].split('=')[1])
            amount = int(words[-1])
            if axis == 'row':
                self.rotate_row(index, amount)
            else:
                self.rotate_col(index, amount)

    def run_instructions(self, instructions):
        for instruction in instructions:
            self.run_instruction(instruction)

    def check_voltage(self):
        return np.sum(self.grid)


def make_screen():
    screen = LittleScreen((6, 50))
    screen.run_instructions(advent_tools.read_input_lines())
    return screen


def run_part_1():
    print(make_screen().check_voltage())


def run_part_2():
    make_screen().show()


if __name__ == '__main__':
    run_part_1()
    run_part_2()