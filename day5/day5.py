import contextlib
import itertools
import functools
import advent_tools
import hashlib

def run_part_1():
    door_id = 'ffykfhsq'
    digits = ''
    count = 0
    while len(digits) < 8:
        to_hash = (door_id + str(count)).encode('utf-8')
        hash = hashlib.md5(to_hash).hexdigest()
        if hash.startswith('0' * 5):
            digits = digits + hash[5]
            print(digits)
        count = count + 1
    print(digits)


def run_part_2():
    door_id = 'ffykfhsq'
    digits = ['_'] * 8
    count = 0
    while '_' in digits[:8]:
        to_hash = (door_id + str(count)).encode('utf-8')
        hash = hashlib.md5(to_hash).hexdigest()
        if hash.startswith('0' * 5):
            position = hash[5]
            digit = hash[6]
            if position.isdigit():
                int_pos = int(position)
                with contextlib.suppress(IndexError):
                    if digits[int_pos] == '_':
                        digits[int_pos] = digit
                        print(''.join(digits[:8]))
        count = count + 1


if __name__ == '__main__':
    # run_part_1()
    run_part_2()