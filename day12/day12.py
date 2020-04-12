import contextlib
import collections
import copy
import functools
import inspect
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

class MonorailComputer(advent_tools.Computer):

    operation = advent_tools.Computer.operation
    return_register = 'a'

    @operation('cpy')
    def copy(self, from_key_or_val, to_key):
        value = self.get_key_or_val(from_key_or_val)
        self.registers[to_key] = value

    def get_key_or_val(self, from_key_or_val):
        try:
            value = int(from_key_or_val)
        except ValueError:
            value = self.registers[from_key_or_val]
        return value

    @operation('inc')
    def increment(self, key):
        self.registers[key] = self.registers[key] + 1

    @operation('dec')
    def decrement(self, key):
        self.registers[key] = self.registers[key] - 1

    @operation('jnz')
    def jump_not_zero(self, ref_key_or_val, offset_key_or_val):
        ref = self.get_key_or_val(ref_key_or_val)
        offset = self.get_key_or_val(offset_key_or_val)
        if ref:
            self.instruction_pointer = self.instruction_pointer + offset - 1


def run_part_1():
    computer = MonorailComputer()
    print(computer.run_input_file())


def run_part_2():
    computer = MonorailComputer()
    computer.registers['c'] = 1
    print(computer.run_input_file())


if __name__ == '__main__':
    run_part_1()
    run_part_2()