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


class State:

    def __init__(self):
        self.generators = collections.defaultdict(set)
        self.microchips = collections.defaultdict(set)
        self.elevator_position = 1

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

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
        for floor in self.get_occupied_floors():
            floor_result = (
                        [str(floor), 'G'] + sorted(self.generators[floor]) + [
                    'M'] + sorted(self.microchips[floor]))
            result.append('_'.join(floor_result))
        result.append('E' + str(self.elevator_position))
        return ';'.join(result)

    def get_occupied_floors(self):
        result = []
        for floor in range (1, 5):
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

    def generate_state_steps(self):
        result = set()
        for delta_elevator in [-1, 1]:
            new_elevator = self.elevator_position + delta_elevator
            for num_microchips in [1, 2]:
                if len(self.microchips[self.elevator_position]) >= num_microchips:
                    for move_microchips in itertools.combinations(
                            self.microchips[self.elevator_position],
                            num_microchips):
                        new_state = copy.deepcopy(self)
                        new_state.elevator_position = new_elevator
                        new_state.microchips[self.elevator_position] = \
                            self.microchips[
                                self.elevator_position].difference(move_microchips)
                        new_state.microchips[new_elevator] = \
                            self.microchips[new_elevator].union(move_microchips)
                        if new_state:
                            result.add(new_state)
            for num_generators in [1, 2]:
                if len(self.generators[self.elevator_position]) >= num_generators:
                    for move_generators in itertools.combinations(
                            self.generators[self.elevator_position], num_generators):
                        new_state = copy.deepcopy(self)
                        new_state.elevator_position = new_elevator
                        new_state.generators[self.elevator_position] = \
                            self.generators[
                                self.elevator_position].difference(move_generators)
                        new_state.generators[new_elevator] = \
                            self.generators[new_elevator].union(move_generators)
                        if new_state:
                            result.add(new_state)
            for microchip in self.microchips[self.elevator_position]:
                for generator in self.generators[self.elevator_position]:
                    new_state = copy.deepcopy(self)
                    new_state.elevator_position = new_elevator
                    new_state.microchips[self.elevator_position].remove(
                        microchip)
                    new_state.microchips[new_elevator].add(microchip)
                    new_state.generators[self.elevator_position].remove(
                        generator)
                    new_state.generators[new_elevator].add(generator)
                    if new_state:
                        result.add(new_state)
        return result


class Final_state(State):

    def __init__(self, other_state):
        super().__init__()
        self.elevator_position = 4
        for floor in other_state.get_occupied_floors():
            self.generators[4].update(other_state.generators[floor])
            self.microchips[4].update(other_state.microchips[floor])


def steps_to_final_state(current_state, final_state):
    queue = collections.deque()
    discovered = {str(current_state): 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[str(state)]
        # if num_steps % 10 == 0:
        #     print(state, num_steps)
        if str(state) == str(final_state):
            return num_steps
        new_states = state.generate_state_steps()
        for new_state in new_states:
            if str(new_state) not in discovered:
                discovered[str(new_state)] = num_steps + 1
                queue.append(new_state)
            elif num_steps + 1 < discovered[str(new_state)]:
                discovered[str(new_state)] = num_steps + 1


def run_part_1():
    initial_state = State()
    initial_state.read_initial_state()
    # print(initial_state)
    final_state = Final_state(initial_state)
    # for state in initial_state.generate_state_steps():
    #     print(state, bool(state))
    # print(final_state)
    # print(bool(final_state))
    start_time = datetime.now()
    print(steps_to_final_state(initial_state, final_state))
    elapsed_time = datetime.now() - start_time
    print(elapsed_time)
    # 641 is too high
    # print(final_state)
    # print(steps_to_final_state(initial_state, final_state))


def run_part_2():
    pass


if __name__ == '__main__':
    run_part_1()
    run_part_2()