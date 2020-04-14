import contextlib
import collections
import copy
import functools
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools

GOAL = 3

EMPTY = 2

WALL = 1


def find_viable_pairs(lines):
    nodes = get_nodes(lines)
    result = []
    for ((xpos1, ypos1, used1, avail1), (xpos2, ypos2, used2, avail2)) in (
                                 itertools.product(nodes, repeat=2)):
        if (xpos1, ypos1) != (xpos2, ypos2) and used1 != 0 and used1 < avail2:
            result.append((xpos1, ypos1, xpos2, ypos2))
    return result


def get_nodes(lines):
    nodes = []
    for line in lines:
        words = line.split()
        name = words[0][15:]
        used = int(words[2][:-1])
        avail = int(words[3][:-1])
        words = name.split('-')
        xpos = int(words[0][1:])
        ypos = int(words[1][1:])
        nodes.append((xpos, ypos, used, avail))
    return nodes


class StorageGrid(advent_tools.PlottingGrid):

    def __init__(self, nodes):
        super().__init__((29, 35))
        for node in nodes:
            xpos, ypos, used, avail = node
            if used > 89:
                self.grid[ypos, xpos] = WALL
            if used == 0:
                self.grid[ypos, xpos] = EMPTY
        self.grid[0, -1] = GOAL

    def move(self):
        count = 0
        y_empty, x_empty = np.argwhere(self.grid == EMPTY)[0]
        y_goal, x_goal = np.argwhere(self.grid == GOAL)[0]
        while x_empty > 1:
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            x_empty = x_empty - 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
        while y_empty > 0:
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            y_empty = y_empty - 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
        while x_empty < 33:
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            x_empty = x_empty + 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
        while x_empty > 0:
            count = count + 1
            x_empty, x_goal, y_empty, y_goal = self.switch_goal_empty(
                x_empty, x_goal, y_empty, y_goal)
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            y_empty = y_empty + 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            x_empty = x_empty - 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            x_empty = x_empty - 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
            count = count + 1
            self.grid[y_empty, x_empty] = 0
            y_empty = y_empty - 1
            self.grid[y_empty, x_empty] = EMPTY
            self.draw()
        count = count + 1
        self.switch_goal_empty(x_empty, x_goal, y_empty, y_goal)
        return count

    def switch_goal_empty(self, x_empty, x_goal, y_empty, y_goal):
        y_empty, x_empty, y_goal, x_goal = y_goal, x_goal, y_empty, x_empty
        self.grid[y_empty, x_empty] = EMPTY
        self.grid[y_goal, x_goal] = GOAL
        self.draw()
        return x_empty, x_goal, y_empty, y_goal


def run_part_1():
    lines = advent_tools.read_input_lines()[2:]
    print(len(find_viable_pairs(lines)))

def run_part_2():
    lines = advent_tools.read_input_lines()[2:]
    nodes = get_nodes(lines)
    grid = StorageGrid(nodes)
    # Also did it on paper by just writing out the steps
    print(7 + 28 + 32 + 5*33 + 1)
    # But it looks pretty cool to animate it
    print(grid.move())


if __name__ == '__main__':
    # run_part_1()
    run_part_2()