#! /bin/python3

import os
import logging
import argparse

from typing import Tuple


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", type=str,
                        help="Folder that is searched for links to be listed and checked.", required=True)

    args = parser.parse_args()

    return args


def is_broken(link_path: str) -> bool:
    """

    :param link_path:
    :return:
    """
    return not os.path.exists(link_path)


def is_relative(link_path: str) -> bool:
    """

    :param link_path:
    :return:
    """
    link_target = os.readlink(link_path)

    return not os.path.isabs(link_target)


def log_link(link_path: str) -> Tuple[bool, bool]:
    """

    :param link_path:
    :return:
    """
    link_is_broken = is_broken(link_path)
    link_is_relative = is_relative(link_path)

    link_target = os.readlink(link_path)

    logging.debug("Found link:")
    logging.debug("%s -> %s" % (link_path, link_target))
    logging.debug("Status: %s" % ("BROKEN" if link_is_broken else "OK"))
    logging.debug("Path: %s" % ("RELATIVE" if link_is_relative else "ABSOLUTE"))
    logging.debug("=" * 30)

    return link_is_broken, link_is_relative


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

    real_folder_path = os.path.realpath(args.folder)

    assert os.path.exists(real_folder_path), "Folder does not exist: '%s'" % args.folder

    links_found = 0
    broken_links_found = 0
    relative_links_found = 0

    for r, d, f in os.walk(real_folder_path):
        for file in f:
            full_path = os.path.join(r, file)
            if os.path.islink(full_path):
                links_found += 1

                is_broken, is_relative = log_link(full_path)

                if is_broken:
                    broken_links_found += 1
                if is_relative:
                    relative_links_found += 1

    logging.debug("Links found: %d" % links_found)
    logging.debug("Number of broken links found: %d" % broken_links_found)
    logging.debug("Number of relative links found: %d" % relative_links_found)


if __name__ == '__main__':
    main()
