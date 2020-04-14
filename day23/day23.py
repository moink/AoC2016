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


class SafeComputer(advent_tools.Computer):

    operation = advent_tools.Computer.operation
    return_register = 'a'

    def __init__(self, program):
        super().__init__()
        self.program = program

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

    @operation('tgl')
    def toggle(self, key):
        offset = self.get_key_or_val(key)
        index = self.instruction_pointer + offset
        try:
            instruction = self.program[index]
        except IndexError:
            pass
        else:
            words = instruction.split()
            operation = words[0]
            num_args = len(inspect.signature(self.operation_map[
                                             operation]).parameters) - 1
            if num_args == 1:
                if operation == 'inc':
                    new_operation = 'dec'
                else:
                    new_operation = 'inc'
            elif num_args == 2:
                if operation == 'jnz':
                    new_operation = 'cpy'
                else:
                    new_operation = 'jnz'
            new_instruction = ' '.join([new_operation] + words[1:])
            self.program[index] = new_instruction

    def run_program(self):
        while True:
            if self.instruction_pointer == 3:
                self.registers['a'] = self.registers['d'] * self.registers['b']
                self.instruction_pointer = 10
            try:
                line = self.program[self.instruction_pointer]
            except IndexError:
                return self.registers[self.return_register]
            self.run_instruction(line)
            self.instruction_pointer = self.instruction_pointer + 1

def run_part_1():
    computer = SafeComputer(advent_tools.read_input_lines())
    computer.registers['a'] = 7
    print(computer.run_program())

def run_part_2():
    computer = SafeComputer(advent_tools.read_input_lines())
    computer.registers['a'] = 12
    print(computer.run_program())


if __name__ == '__main__':
    run_part_1()
    run_part_2()