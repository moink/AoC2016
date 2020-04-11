import collections
import itertools
import functools
import advent_tools


def get_sector_id_of_valid(room):
    if check_if_room_valid(room):
        return int(room.split('[')[0].split('-')[-1])
    return 0


def check_if_room_valid(room):
    first_part, second_part = room.split('[')
    count = collections.Counter(first_part)
    by_count = collections.defaultdict(str)
    for char, num in count.most_common():
        if char.isalpha():
            by_count[num] = by_count[num] + char
    concat = ''
    for num, part_str in by_count.items():
        concat = concat + ''.join(sorted(part_str))
    check_sum = concat[:5] + ']'
    valid_room = check_sum == second_part
    return valid_room


def run_part_1():
    rooms = advent_tools.read_input_lines()
    valid = [get_sector_id_of_valid(room) for room in rooms]
    print(sum(valid))


def run_part_2():
    rooms = advent_tools.read_input_lines()
    for room in rooms:
        result = ''
        if check_if_room_valid(room):
            sector_id = get_sector_id_of_valid(room)
            for char_in in room:
                if char_in == '-':
                    result = result + ' '
                elif char_in.isalpha():
                    num_in = ord(char_in) - 97
                    num_out = (num_in + sector_id) % 26
                    result = result + chr(num_out + 97)
            print(sector_id, result)



if __name__ == '__main__':
    run_part_1()
    run_part_2()