#! /usr/bin/python3

"""
Will fix date formats and optionally preprend a prefix string to a filename.
"""

import os
import datetime
import argparse
import logging

from typing import Optional


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str,
                        help="Absolute path to input file.", required=True)
    parser.add_argument("--prefix", type=str,
                        help="Add this string to the beginning of file names", required=False)

    parser.add_argument("--dry-run", action="store_true",
                        help="Do not change any file names, just print what would change hypothetically.")

    args = parser.parse_args()

    return args


def parse_date(date_string: str) -> Optional[datetime.datetime]:
    """

    :param date_string:
    :return:
    """
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return None


def canonicalize(filename: str) -> str:
    """
    """

    parts = filename.split(".")

    new_parts = []

    for part in parts:
        datetime_object = parse_date(part)

        if datetime_object is None:
            new_part = part
        else:
            new_part = datetime_object.strftime("%Y-%m-%d")

        new_parts.append(new_part)

    new_filename = ".".join(new_parts)

    return new_filename


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    # logging.debug(args)

    input_path = args.input

    assert os.path.isabs(input_path), "Can only use absolute paths."

    basename = os.path.basename(input_path)
    dirname = os.path.dirname(input_path)

    new_basename = canonicalize(basename)

    if args.prefix is not None:
        new_basename = args.prefix + new_basename

    output_path = os.path.join(dirname, new_basename)

    logging.info("\t%s -> %s" % (input_path, output_path))

    if not args.dry_run:
        os.rename(input_path, output_path)


if __name__ == '__main__':
    main()
