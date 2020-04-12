"""Tools to help solve advent of code problems faster"""
import abc
import collections
import contextlib
import copy
import datetime
import hashlib
import itertools
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
        plt.colorbar()
        plt.show()


class StateForGraphs(abc.ABC):
    """A starter for a state class for use in graph traversal

    One requirement to make this work in number_of_bfs_steps, below, is to
    implement __hash__ and __eq__. What I have found is the simplest way to do
    that is to make a unique string representation of each step, and use
    that to hash and compare the object. That's what's used by default here,
    so that only __str__ must be implemented by the child object. But if
    that doesn't work, just override __hash__ and __eq__ directly.

    The other requirement is to implement possible_next_states,
    which provides the edges of the graphs connected to this node, or state.
    That's where the real meat of the problem will end up.

    Notes for optimization of breadth-first searches:
        - If two states are equivalent in some way, as in the steps required
            don't depend on any differences between them, make their string
            representations the same, so that they compare as equal
        - Look for patterns in the best strategies. Don't return paths
            guaranteed to be suboptimal from possible_next_states
    """

    @abc.abstractmethod
    def __str__(self):
        """Return string representation. Used for hashing and comparing equal
        """
        pass

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    @abc.abstractmethod
    def possible_next_states(self):
        """Create and return states reachable from this one in one step

        This is where the details of the problem go. This should return a
        set of valid states reachable from the current state in one step.

        For optimization reasons, it is best to reject steps known to be
        globally suboptimal in this method, by not returning them. The fewer
        states this method returns, the faster the search will go. But if
        the globally optimal next state is not contained in the result,
        the search will not find the minimum number of states.

        Returns:
            Set of StateForGraphs
                States reachable from this state in one step
        """
        return set(copy.deepcopy(self))


def number_of_bfs_steps(current_state, final_state):
    """Perform a breadth-first search and return number of steps taken

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.
        final_state: StateForGraphs
            The state at the end of the search; the leaf being searched for

    Returns:
        The number of steps required to get from current_state to
        final_state, using state.possible_next_states to find states
        reachable in one step from the current state

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, and possible_next_states
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        new_states = state.possible_next_states()
        for new_state in new_states:
            if new_state == final_state:
                return num_steps + 1
            if new_state not in discovered:
                discovered[new_state] = num_steps + 1
                queue.append(new_state)


def number_of_reachable_in_steps(current_state, max_steps):
    """Find the number of states reachable from this one in max steps

    Use a breadth-first search to figure out how many states are reachable
    from the current state, when each state can provide the steps it can
    reach in one state.

    Args:
        current_state: StateForGraphs
            The state at the beginning of the search; the root of the tree.
        max_steps: int
            The maximum number of steps to take, using
            state.possible_next_states to find states reachable in one step
            from the current state

    Returns:
        number_reachable : int
            Number of distinct states reachable from current_state,
            with fewer or equal to max_steps steps.

    See Also: StateForGraphs
        to understand the required methods for the states used in the graph.
        The states must implement __hash__, __eq__, and possible_next_states
    """
    queue = collections.deque()
    discovered = {current_state: 0}
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        num_steps = discovered[state]
        if num_steps < max_steps:
            new_states = state.possible_next_states()
            for new_state in new_states:
                if new_state not in discovered:
                    discovered[new_state] = num_steps + 1
                    queue.append(new_state)
    return len(discovered)

class Computer(abc.ABC):
    """A virtual machine base class for running custom assembly languages

    Seems that Topaz likes to put problems that require virtual machines
    with registers that run his own small assembly languages. There was one
    in 2015 (day 23) and one in 2016 (day 12) and a much more complex one
    used on many days in 2019. This probably doesn't implement enough for
    the 2019 IntCode computer but it works for 2015 and 2016.

    To use this, inherit from this class. Include the following two lines at
    the start of the class:
        operation = advent_tools.Computer.operation
        return_register = 'a'
    (setting return_register to the register that the question requests) and
    then decorate all assembly commands with @operation('cmd') where cmd is
    the first word of the instruction to call that command. The operations
    can use self.registers to access the computer's registers
    """

    operation_map = {}

    def __init__(self):
        self.registers = collections.defaultdict(int)
        self.instruction_pointer = 0

    @property
    @abc.abstractmethod
    def return_register(self):
        """The register to return at the end of the program"""
        pass

    @classmethod
    def operation(cls, instruction_first_word):
        """Mark a method as an operation

        Args:
            instruction_first_word: str
                First word of the instruction, the part that indicates which
                operation to run

        Returns:
            A decorator which marks the method as an operation
        """
        def decorator(func):
            """Decorator to mark a method as an operation"""
            cls.operation_map[instruction_first_word] = func
            return func
        return decorator

    def run_instruction(self, instruction):
        """Run a single instruction

        Using the first word of the instruction, figure out what operation
        to run. Pass the rest of the words of the instruction as an argument.

        Args:
            instruction: str
                Instruction to run. Must start with a valid operation
                identifier (key of self.operation_map)

        Returns:
            None
        """
        words = instruction.split()
        func = self.operation_map[words[0]]
        func(self, *words[1:])

    def run_program(self, program):
        """Run a list of instructions through the virtual machine

        The program terminates when the instruction pointer moves past the
        end of the program

        Args:
            program: [str]
                Instructions, each of which starts with a valid operation
                identifier
        Returns:
            int
                Contents of the return register when the program terminates
        """
        while True:
            try:
                line = program[self.instruction_pointer]
            except IndexError:
                return self.registers[self.return_register]
            self.run_instruction(line)
            self.instruction_pointer = self.instruction_pointer + 1

    def run_input_file(self):
        """Run the contents of today's input file through the virtual machine

        Returns:
            int
                Contents of the return register when the program terminates
        """
        program = read_input_lines()
        return self.run_program(program)


def md5_increment(salt):
    """Append an increasing integer to the salt and run an md5 hash on it

    Args:
        salt: str
            First characters of the string to be hashed. The remaining
            characters are increasing integers starting at 0

    Yields:
        md5_hash : str
            An md5 hash of the salt prepended to an integer
    """
    for count in itertools.count():
        to_hash = (salt + str(count)).encode('utf-8')
        hashed = hashlib.md5(to_hash).hexdigest()
        yield count, hashed


if __name__ == '__main__':
    # start_coding_today()
    today = 15
    start_coding(today)
