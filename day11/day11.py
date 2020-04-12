import contextlib
import collections
import copy
import functools
import itertools
from datetime import datetime

import numpy as np
import pandas as pd
import re

import advent_tools


class State(advent_tools.StateForGraphs):

    def __init__(self):
        self.generators = collections.defaultdict(set)
        self.microchips = collections.defaultdict(set)
        self.elevator_position = 1

    def __bool__(self):
        if self.elevator_position < 1:
            return False
        if self.elevator_position > 4:
            return False
        for floor, chips in self.microchips.items():
            for chip in chips:
                if (self.generators[floor]
                        and chip not in self.generators[floor]):
                    return False
        return True

    def __str__(self):
        result = []
        replacements = {}
        elem_count = 0
        for floor in self.get_occupied_floors():
            floor_result = [str(floor), 'G']
            for gen in sorted(self.generators[floor]):
                if gen not in replacements:
                    replacements[gen] = str(elem_count)
                    elem_count = elem_count + 1
                floor_result.append(replacements[gen])
            floor_result.append('M')
            for mic in sorted(self.microchips[floor]):
                if mic not in replacements:
                    replacements[mic] = str(elem_count)
                    elem_count = elem_count + 1
                floor_result.append(replacements[mic])
            result.append('_'.join(floor_result))
        result.append('E' + str(self.elevator_position))
        return ';'.join(result)

    def get_occupied_floors(self):
        result = []
        for floor in range(1, 5):
            if ((floor in self.generators.keys() and self.generators[floor])
                    or (floor in self.microchips.keys()
                        and self.microchips[floor])):
                result.append(floor)
        return result

    def read_initial_state(self):
        lines = advent_tools.read_input_lines()
        gen_pattern = r'a ([\w]+) generator'
        mc_pattern = r'a ([\w]+)-compatible microchip'
        for floor, line in enumerate(lines, start=1):
            for match in re.finditer(gen_pattern, line):
                self.generators[floor].add(match.groups()[0])
            for match in re.finditer(mc_pattern, line):
                self.microchips[floor].add(match.groups()[0])

    def possible_next_states(self):
        result = set()
        # Only consider moving things down if there are things below the
        # floor we are on
        if any((floor < self.elevator_position for
                floor in self.get_occupied_floors())):
            move_numbers = {1: [2, 1], -1: [1, 2]}
        else:
            move_numbers = {1: [2, 1]}
        for delta_elevator, nums_things_to_move in move_numbers.items():
            new_elevator = self.elevator_position + delta_elevator
            floor_microchips = self.microchips[self.elevator_position]
            floor_generators = self.generators[self.elevator_position]
            for move_item_count in nums_things_to_move:
                if len(floor_microchips) >= move_item_count:
                    for move_microchips in itertools.combinations(
                            floor_microchips, move_item_count):
                        new_state = self.state_moving_stuff(
                            move_microchips, [], new_elevator)
                        if new_state:
                            result.add(new_state)
                if len(floor_generators) >= move_item_count:
                    for move_generators in itertools.combinations(
                            floor_generators, move_item_count):
                        new_state = self.state_moving_stuff(
                            [], move_generators, new_elevator)
                        if new_state:
                            result.add(new_state)
                if (move_item_count == 2):
                    # Only consider bringing paired microchips & generators
                    # togethr
                    for microchip in floor_microchips:
                        if microchip in floor_generators:
                            new_state = self.state_moving_stuff(
                                [microchip], [microchip], new_elevator)
                            if new_state:
                                result.add(new_state)
                if result:
                    # if we are going up, and we can move 2 items, do so and
                    # don't bother trying to move 1 item
                    # And if we are going down, and we can move 1 item,
                    # do so and don't bother trying to move 2 items
                    # Credit: Peter Tseng
                    # https://github.com/petertseng/adventofcode-rb-2016/blob/master/11_chips_and_generators.rb
                    break
        return result

    def state_moving_stuff(self, move_microchips, move_generators,
                           new_elevator):
        new_state = copy.deepcopy(self)
        new_state.elevator_position = new_elevator
        new_state.microchips[self.elevator_position] = self.microchips[
            self.elevator_position].difference(move_microchips)
        new_state.microchips[new_elevator] = self.microchips[
            new_elevator].union(move_microchips)
        new_state.generators[self.elevator_position] = self.generators[
            self.elevator_position].difference(move_generators)
        new_state.generators[new_elevator] = self.generators[
            new_elevator].union(move_generators)
        return new_state


class Final_state(State):

    def __init__(self, other_state):
        super().__init__()
        self.elevator_position = 4
        for floor in other_state.get_occupied_floors():
            self.generators[4].update(other_state.generators[floor])
            self.microchips[4].update(other_state.microchips[floor])


def run_part_1():
    initial_state = State()
    initial_state.read_initial_state()
    final_state = Final_state(initial_state)
    start_time = datetime.now()
    print(advent_tools.number_of_bfs_steps(initial_state, final_state))
    elapsed_time = datetime.now() - start_time
    print(elapsed_time)


def run_part_2():
    initial_state = State()
    initial_state.read_initial_state()
    initial_state.microchips[1].update(['elerium', 'dilithium'])
    initial_state.generators[1].update(['elerium', 'dilithium'])
    final_state = Final_state(initial_state)
    print(advent_tools.number_of_bfs_steps(initial_state, final_state))


if __name__ == '__main__':
    run_part_1()
    # run_part_2()
