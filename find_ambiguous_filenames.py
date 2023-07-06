#! /usr/bin/python3

"""
Find duplicate IDs in filenames
"""

import os
import argparse
import logging

from collections import Counter
from typing import List, Optional


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", type=str,
                        help="Folder with files.", required=True)

    parser.add_argument("--ignores", type=str, nargs="+",
                        help="Filename components to ignore.", required=False)

    args = parser.parse_args()

    return args


def get_ambiguous_elements(filenames: List[str]) -> List[str]:
    """

    :param filenames:
    :return:
    """

    return [k for k, v in Counter(filenames).items() if v > 1]


def remove_ignore_components(filenames: List[str], ignores: Optional[List[str]] = None) -> List[str]:
    """

    :param filenames:
    :param ignores:
    :return:
    """
    if ignores is None:
        return filenames

    new_filenames = []

    for filename in filenames:
        new_filename = filename
        for ignore in ignores:
            new_filename = new_filename.replace(ignore, "")
        new_filename = new_filename.replace(".", "")

        new_filenames.append(new_filename)

    return new_filenames


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

    filenames = list(os.listdir(args.folder))

    print("filenames[:10]")
    print(filenames[:10])

    filenames_ignored = remove_ignore_components(filenames, args.ignores)

    print("filenames_ignored[:10]")
    print(filenames_ignored[:10])

    ambiguous_filenames = get_ambiguous_elements(filenames_ignored)

    print("All ambiguous filenames:")
    print(ambiguous_filenames)
    print("Total number of ambiguous filenames: %d" % len(ambiguous_filenames))


if __name__ == '__main__':
    main()
