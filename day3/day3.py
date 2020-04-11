import itertools
import functools
import advent_tools


def validate_triangle(triangle):
    a, b, c = triangle
    return (a + b > c) and (a + c > b) and (b + c > a)


def read_vertical_triangles(data):
    triangles = []
    for start_line in range(0, len(data), 3):
        for i in range(3):
            triangle = [data[start_line + j][i] for j in range(3)]
            triangles.append(triangle)
    return triangles


def read_data():
    data = [[int(num) for num in line.split()] for line in
            advent_tools.read_input_lines()]
    return data


def count_valid(triangles):
    valid = [validate_triangle(triangle) for triangle in triangles]
    print(sum(valid))


def run_part_1():
    triangles = read_data()
    count_valid(triangles)


def run_part_2():
    data = read_data()
    triangles = read_vertical_triangles(data)
    count_valid(triangles)


if __name__ == '__main__':
    run_part_1()
    run_part_2()