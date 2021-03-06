#!/usr/bin/env python3
"""Make student groups, ensuring that students work with those they have worked
with the fewest times before.
"""
import argparse
import sys
from typing import Iterable

from groupmaker.counting import count_pairs
from groupmaker.file_io import read_group_configs, read_students, \
    write_group_config
from groupmaker.pairing import calc_pairs_in_group_configs
from groupmaker.solver import solve_for_min_scoring_groups
from groupmaker.table import print_student_pair_count_matrix


def _run_main(
        students_file_path: str, group_size: int, historical_groups_file_paths:
        Iterable[str], verbosity: int
) -> None:
    """Read a list of students, a requested group size, and historical groups,
    then generate a new group of the requested size with the fewest students
    that have worked together before.
    """
    with open(students_file_path) as students_file:
        students = read_students(students_file)
    historical_group_configs = list(
        read_group_configs(historical_groups_file_paths)
    )

    historical_pair_counts = count_pairs(
        calc_pairs_in_group_configs(historical_group_configs)
    )

    if verbosity > 0:
        print_student_pair_count_matrix(
            students, historical_pair_counts, file=sys.stderr
        )

    min_scoring_group_config = solve_for_min_scoring_groups(
        students, group_size, historical_pair_counts
    )
    write_group_config(min_scoring_group_config)


def main() -> None:
    """Command line script entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-n',
        dest='group_size',
        metavar='GROUP_SIZE',
        type=int,
        default=3,
        help='form groups of this many students (default: %(default)s)'
    )
    parser.add_argument(
        '-v',
        dest='verbosity',
        action='count',
        default=0,
        help='print out historical pair counts to stderr before calculating '
        'new groups'
    )
    parser.add_argument(
        'student_file_path',
        metavar='STUDENT_FILE',
        help='file containing student names, one per line'
    )
    parser.add_argument(
        'historical_groups_file_paths',
        metavar='GROUP_FILE',
        nargs='*',
        help='files containing previous groups, one student per line, one '
        'blank line between groups'
    )

    args = parser.parse_args()
    _run_main(
        args.student_file_path, args.group_size,
        args.historical_groups_file_paths, args.verbosity
    )
