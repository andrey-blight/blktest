import sys
import math


def print_progress(current: int, total: int, bar_length: int = 40) -> None:
    """
    Print a progress bar in console.

    :param current: current iteration
    :param total: total iterations
    :param bar_length: length of bar
    """

    progress_percent = current / total
    block = int(bar_length * progress_percent)
    bar = "=" * block + "-" * (bar_length - block)
    percent = progress_percent * 100

    # print in one line
    sys.stdout.write(f"\r[{bar}] {percent:.2f}%")
    sys.stdout.flush()

    if current == total:  # if this is last line of progress line add \n to stdout
        print()


def generate_parameters(num_tests: int, start: int = 1, stop: int = 256) -> list[int]:
    """
    Generate iodepth parameters from start and stop

    :param start: iodepth minimum value.
    :param stop: iodepth maximum value.
    :param num_tests: number of iodepth parameters.
    :return: list of iodepth.
    """
    # Step by log
    step = (math.log2(stop) - math.log2(start)) / (num_tests - 1)

    # Generate iodepth
    params = [round(math.pow(2, math.log2(start) + i * step)) for i in range(num_tests)]

    # Delete equal and sort
    return sorted(set(params))


def parse_args():
    """
    Get arguments from command line.

    :return: test name, file name, plot file name
    """
    return sys.argv[1:]
