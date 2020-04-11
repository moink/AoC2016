import itertools
import functools
import advent_tools

def create_mapping(max_width):
    result = {}
    lengths = list(range(1, max_width, 2)) + list(range(max_width, 0, -2))
    num = 0
    for y, length in enumerate(lengths):
        for offset in range(length):
            x = (max_width - length) // 2 + offset
            num = num + 1
            result[str(hex(num)[2:]).upper()] = (x, y)
    return result

MAPPING = create_mapping(5)

def follow_instruction(instruction, start_num):
    y, x = divmod(start_num - 1, 3)
    for direction in instruction:
        if direction == 'R':
            x = min(x + 1, 2)
        elif direction == 'L':
            x = max(x - 1, 0)
        elif direction == 'U':
            y = max(y - 1, 0)
        elif direction == 'D':
            y = min(y + 1, 2)
    final_num = 3 * y + x + 1
    return final_num


def convert_digit(start_num):
    return MAPPING[start_num]


def convert_back(x, y):
    reverse_mapping = {val: key for key, val in MAPPING.items()}
    return reverse_mapping[(x, y)]


def try_dir(old_point, new_point):
    if new_point in MAPPING.values():
        return new_point
    else:
        return old_point


def follow_instruction2(instruction, start_num):
    x, y = convert_digit(start_num)
    for direction in instruction:
        if direction == 'R':
            x, y = try_dir((x, y), (x + 1 , y))
        elif direction == 'L':
            x, y = try_dir((x, y), (x - 1, y))
        elif direction == 'U':
            x, y = try_dir((x, y), (x, y - 1))
        elif direction == 'D':
            x, y = try_dir((x, y), (x, y + 1))
    final_num = convert_back(x, y)
    return final_num



def run_part_1():
    instructions = advent_tools.read_input_lines()
    digits = []
    digit = 5
    for line in instructions:
        digit = follow_instruction(line, digit)
        digits.append(str(digit))
    print(''.join(digits))


def run_part_2():
    instructions = advent_tools.read_input_lines()
    digits = []
    digit = '5'
    for line in instructions:
        digit = follow_instruction2(line, digit)
        digits.append(digit)
    print(''.join(digits))




if __name__ == '__main__':
    run_part_1()
    run_part_2()
