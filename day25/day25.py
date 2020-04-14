import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

class MonorailComputer(advent_tools.Computer):

    operation = advent_tools.Computer.operation
    return_register = 'a'

    def __init__(self):
        super().__init__()
        self.outputs = []
        self.done = False
        self.expected_outputs = itertools.cycle([0, 1])

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

    @operation('out')
    def output(self, key_or_val):
        val = self.get_key_or_val(key_or_val)
        expected = next(self.expected_outputs)
        if val != expected:
            self.done = True

    def run_program(self, program):
        """Run a list of instructions through the virtual machine

        The program terminates when the instruction pointer moves past the
        end of the program

        Args:
            program: [str]
                Instructions, each of which starts with a valid operation
                identifier
        Returns:
            int
                Contents of the return register when the program terminates
        """
        while not self.done:
            # if self.instruction_pointer == 2:
            #     self.registers['d'] = self.registers['d'] + 182 * 14
            #     self.instruction_pointer = 8
            # elif self.instruction_pointer == 11:
            #     self.registers['a'] = self.registers['b'] // 2
            #     self.instruction_pointer == 19
            try:
                line = program[self.instruction_pointer]
            except IndexError:
                return self.registers[self.return_register]
            self.run_instruction(line)
            self.instruction_pointer = self.instruction_pointer + 1

def run_part_1():
    count = 0
    while True:
        computer = MonorailComputer()
        count = count + 1
        print(count)
        computer.registers['a'] = count
        computer.run_input_file()


def run_part_2():
    pass


if __name__ == '__main__':
    run_part_1()
    run_part_2()