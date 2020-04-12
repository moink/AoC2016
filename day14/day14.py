import contextlib
import collections
import copy
import functools
import hashlib
import itertools
import numpy as np
import pandas as pd
import re

import advent_tools


def md5_increment_2016(salt):
    for count in itertools.count():
        the_hash = (salt + str(count))
        for i in range(2017):
            the_hash = hashlib.md5(the_hash.encode('utf-8')).hexdigest()
        yield count, the_hash


def find_sixty_four_indexes(hash_series):
    triple_pattern = r'(.)\1{2,}'
    indexes = set()
    watching = []
    while len(indexes) < 128:
        count, test_str = next(hash_series)
        for char, prev_count in watching:
            if (char * 5) in test_str:
                indexes.add(prev_count)
        watching = [(key, old_count) for (key, old_count) in watching
                    if count - old_count < 1000]
        match = re.search(triple_pattern, test_str)
        if match:
            char = match.groups()[0]
            watching.append((char, count))
    return sorted(indexes)[63]

def run_part_1():
    salt = 'cuanljph'
    print(find_sixty_four_indexes(advent_tools.md5_increment(salt)))


def run_part_2():
    salt = 'cuanljph'
    print(find_sixty_four_indexes(md5_increment_2016(salt)))


if __name__ == '__main__':
    run_part_1()
    run_part_2()