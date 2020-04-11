import contextlib
import collections
import functools
import itertools
import re
import unittest

import advent_tools

def split_brackets(ip_address):
    outside = ['']
    inside = []
    in_brackets = False
    for pos, char in enumerate(ip_address):
        if char == '[':
            in_brackets = True
            inside.append('')
        elif char == ']':
            in_brackets = False
            outside.append('')
        elif in_brackets:
            inside[-1] = inside[-1] + char
        else:
            outside[-1] = outside[-1] + char
    return inside, outside


def check_tls(ip_address):
    inside, outside = split_brackets(ip_address)
    inside_abba = any(check_abba(test_str) for test_str in inside)
    outside_abba = any(check_abba(test_str) for test_str in outside)
    return outside_abba and not inside_abba


def reverse_tuples(data):
    return {(b, a) for (a, b) in data}


def check_ssl(ip_address):
    inside, outside = split_brackets(ip_address)
    out_aba = get_aba(outside)
    in_aba = get_aba(inside)
    in_bab = reverse_tuples(in_aba)
    matches = out_aba.intersection(in_bab)
    return bool(matches)


def check_abba(test_str):
    pattern = r'.*(?P<first>[a-z])(?P<second>[a-z])(?P=second)(?P=first)'
    matches = re.finditer(pattern, test_str)
    for match in matches:
        groups = match.groups()
        if groups[0] != groups[1]:
            return True
    return False


def get_aba(test_str):
    pattern = r'(?=(?P<first>[a-z])(?P<second>[a-z])(?P=first))'
    result = get_match_groups(pattern, test_str)
    return result


def get_match_groups(pattern, test_strings):
    result = set()
    for test_str in test_strings:
        matches = re.finditer(pattern, test_str)
        for match in matches:
            groups = match.groups()
            if groups[0] != groups[1]:
                result.add(groups)
    return result


def run_part_1():
    print(advent_tools.count_times_true(check_tls))


def run_part_2():
    print(advent_tools.count_times_true(check_ssl))


if __name__ == '__main__':
    run_part_1()
    run_part_2()
