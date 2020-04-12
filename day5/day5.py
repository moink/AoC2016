import contextlib
import itertools
import functools
import advent_tools
import hashlib

def run_part_1():
    door_id = 'ffykfhsq'
    digits = ''
    hash_series = advent_tools.md5_increment(door_id)
    while len(digits) < 8:
        hash = next(hash_series)
        if hash.startswith('0' * 5):
            digits = digits + hash[5]
            print(digits)
    print(digits)


def run_part_2():
    door_id = 'ffykfhsq'
    digits = ['_'] * 8
    hash_series = advent_tools.md5_increment(door_id)
    while '_' in digits[:8]:
        hash = next(hash_series)
        if hash.startswith('0' * 5):
            position = hash[5]
            digit = hash[6]
            if position.isdigit():
                int_pos = int(position)
                with contextlib.suppress(IndexError):
                    if digits[int_pos] == '_':
                        digits[int_pos] = digit
                        print(''.join(digits[:8]))


if __name__ == '__main__':
    # run_part_1()
    run_part_2()