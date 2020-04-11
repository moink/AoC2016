import itertools
import functools
import advent_tools


def run_part_1():
    with open('input.txt') as in_file:
        str_directions = in_file.read().strip().split(', ')
    directions = [(dir[0], int(dir[1:])) for dir in str_directions]
    x = 0
    y = 0
    facing = 0
    for direction, amount in directions:
        if direction== 'L':
            facing = (facing - 1) % 4
        else:
            facing = (facing + 1) % 4
        if facing == 0:
            y = y - amount
        elif facing== 1:
            x = x + amount
        elif facing == 2:
            y = y + amount
        else:
            x = x - amount
    print(abs(x) + abs(y))

def run_part_2():
    with open('input.txt') as in_file:
        str_directions = in_file.read().strip().split(', ')
    directions = [(dir[0], int(dir[1:])) for dir in str_directions]
    x, y = follow_directions(directions)
    print(abs(x) + abs(y))


def follow_directions(directions):
    x = 0
    y = 0
    facing = 0
    visited = {(0, 0)}
    for direction, amount in directions:
        if direction == 'L':
            facing = (facing - 1) % 4
        else:
            facing = (facing + 1) % 4
        if facing == 0:
            for i in range(1, amount + 1):
                y = y + 1
                if (x, y) in visited:
                    return x, y
                visited.add((x, y))
        elif facing == 1:
            for i in range(1, amount + 1):
                x = x + 1
                if (x, y) in visited:
                    return x, y
                visited.add((x, y))
        elif facing == 2:
            for i in range(1, amount + 1):
                y = y - 1
                if (x, y) in visited:
                    return x, y
                visited.add((x, y))
        else:
            for i in range(1, amount + 1):
                x = x - 1
                if (x, y) in visited:
                    return x, y
                visited.add((x, y))
        # print(direction, amount, visited)


if __name__ == '__main__':
    # run_part_1()
    run_part_2()