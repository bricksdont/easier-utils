#! /bin/python3

import os
import logging
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", type=str,
                        help="Folder that is searched for links to be replaced.", required=True)
    parser.add_argument("--string-before", type=str,
                        help="String to be replaced in path that symlinks are pointing to.", required=False,
                        default="/net/cephfs/shares/volk.cl.uzh/EASIER")
    parser.add_argument("--string-after", type=str,
                        help="String to be inserted as replacement in path that symlinks are pointing to.", required=False,
                        default="/shares/easier.volk.cl.uzh")
    parser.add_argument("--dry-run", action="store_true",
                        help="Do not change any symlinks, just print what would change hypothetically.")

    args = parser.parse_args()

    return args


def replace_link(link_path: str, before: str, after: str, dry_run: bool = False) -> bool:
    """

    :param link_path:
    :param before:
    :param after:
    :param dry_run:
    :return: True if this link was changed
    """

    old_link_target = os.readlink(link_path)

    if before not in old_link_target:
        logging.debug("Skipping irrelevant link: %s -> %s" % (link_path, old_link_target))
        return False

    new_link_target = old_link_target.replace(before, after)

    if dry_run:
        logging.debug("Could remove old link: %s -> %s" % (link_path, old_link_target))
        logging.debug("Could create new link: %s -> %s" % (link_path, new_link_target))
        logging.debug("=" * 30)

        return False

    logging.debug("Removing old link: %s -> %s" % (link_path, old_link_target))
    os.unlink(link_path)

    logging.debug("Creating new link: %s -> %s" % (link_path, new_link_target))
    os.symlink(new_link_target, link_path)

    logging.debug("=" * 30)

    return True


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

    if args.dry_run:
        logging.debug("Dry run, will not actually change any symlinks.")

    real_folder_path = os.path.realpath(args.folder)

    assert os.path.exists(real_folder_path), "Folder does not exist: '%s'" % args.folder

    links_found_total = 0
    links_changed = 0

    for r, d, f in os.walk(real_folder_path):
        for file in f:
            full_path = os.path.join(r, file)
            if os.path.islink(full_path):
                links_found_total += 1

                link_was_changed = replace_link(full_path,
                                                before=args.string_before,
                                                after=args.string_after,
                                                dry_run=args.dry_run)

                if link_was_changed:
                    links_changed += 1

    logging.debug("Total number of links found: %d" % links_found_total)
    logging.debug("Links changed: %d" % links_changed)


if __name__ == '__main__':
    main()
