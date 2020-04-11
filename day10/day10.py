import contextlib
import collections
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

class Bot:

    def __init__(self, words, bot_dict, output_dict):
        self.bot_dict = bot_dict
        self.output_dict = output_dict
        self.ident = int(words[1])
        self.low_to = (words[5], int(words[6]))
        self.high_to = (words[-2], int(words[-1]))
        self.given = set()

    def give(self, number):
        self.given.add(number)
        if (17 in self.given) and (61 in self.given):
            print('Part 1: ', self.ident)
        if len(self.given) == 2:
            self.give_away(min, self.low_to)
            self.give_away(max, self.high_to)

    def give_away(self, fun, give_to):
        if give_to[0] == 'bot':
            self.bot_dict[give_to[1]].give(fun(self.given))
        else:
            self.output_dict[give_to[1]] = fun(self.given)


def run_both_parts():
    instructions = advent_tools.read_input_lines()
    bot_dict = {}
    output_dict = {}
    values = []
    for inst in instructions:
        words = inst.split()
        if (words[0] == 'bot'):
            bot_num = int(words[1])
            bot_dict[bot_num] = Bot(words, bot_dict, output_dict)
        else:
            value = int(words[1])
            bot_num = int(words[-1])
            values.append((bot_num, value))
    for bot_num, value in values:
        bot_dict[bot_num].give(value)
    print('Part 2: ', output_dict[0] * output_dict[1] * output_dict[2])


if __name__ == '__main__':
    run_both_parts()