"""Tools to help solve advent of code problems faster"""
import contextlib
import datetime
import os
import shutil
import urllib.request

from matplotlib import pyplot as plt
import numpy as np

def set_up_directory(day):
    """Make a new directory for working on an advent of code problem

    Args:
        day: int
            day of the month to work on

    Returns:
        new_dir: str
            path to the directory for that day
    """
    this_dir = os.path.dirname(__file__)
    new_dir = os.path.join(this_dir, 'day' + str(day))
    with contextlib.suppress(FileExistsError):
        os.mkdir(new_dir)
    new_file_name = os.path.join(new_dir, 'day' + str(day) + '.py')
    template_file_name = os.path.join(this_dir, 'template.py')
    if not(os.path.exists(new_file_name)):
        shutil.copy(template_file_name, new_file_name)
    return new_dir


def download_input_data(day, new_dir):
    """Download input data for an advent of code problem

    Args:
        day: int
            day of the month to work on
        new_dir: str
            path to the directory for that day

    Returns:
        None
    """
    with open('session_cookie.txt') as cookie_file:
        session_cookie = cookie_file.read()
    url = f'https://adventofcode.com/2016/day/{day}/input'
    opener = urllib.request.build_opener()
    opener.addheaders = [('cookie', 'session=' + session_cookie)]
    urllib.request.install_opener(opener)
    input_file = os.path.join(new_dir, 'input.txt')
    urllib.request.urlretrieve(url, input_file)


def start_coding(day):
    """Prepare to code an advent of code problem

    Args:
        day: int
            day of the month to work on

    Returns:
        None
    """
    new_dir = set_up_directory(day)
    download_input_data(day, new_dir)


def start_coding_today():
    """Prepare to code today's advent of code problem"""
    day_of_month = datetime.datetime.today().day
    start_coding(day_of_month)

def read_input_lines():
    """Open today's input data and return it as a list of lines

    Returns:
        [str]
            Lines in 'input.txt'
    """
    with open('input.txt') as in_file:
        data = in_file.read().strip().splitlines()
    return data

def read_whole_input():
    """Open today's input data and return it as a single string

    Returns:
        str
            Contents of 'input.txt'
    """
    with open('input.txt') as in_file:
        data = in_file.read().strip()
    return data

def count_times_true(function):
    """Count the number of times some function is true for the input lines

    Args:
        function: callable
            A function that takes a string and returns a boolean

    Returns:
        count: int
            The number of times the function returns True, when evaluated
            over each line of the file 'input.txt'
    """
    strings = read_input_lines()
    valid = [function(string) for string in strings]
    return sum(valid)


class PlottingGrid:
    """A tool for maintaining and plotting a grid of numbers

    Not abstract, since it works on its own, but designed to be inherited
    with some methods added that manipulate self.grid between construction
    and showing
    """

    def __init__(self, shape):
        """Constructor

        Args:
            shape: (int, int)
                Number of rows and number of columns in the grid
        """
        self.grid = np.zeros(shape)

    def show(self):
        """Show the grid in a new window

        Execution will be suspended until the window is closed

        Returns:
            None
        """
        plt.clf()
        plt.imshow(self.grid)
        plt.show()

if __name__ == '__main__':
    # start_coding_today()
    today = 10
    start_coding(today)