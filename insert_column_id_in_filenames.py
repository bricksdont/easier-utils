#! /bin/python3

import argparse
import logging
import os

from typing import Set


DATE_TO_COLUMN_ID_SRF = {'2021-03-16': '000019', '2021-02-25': '000038', '2021-03-08': '000026',
                         '2020-05-04': '000340', '2020-03-25': '000381', '2021-01-04': '000090',
                         '2021-01-27': '000067', '2021-03-17': '000018', '2020-03-13': '000398',
                         '2021-02-05': '000058', '2021-01-14': '000080', '2020-03-23': '000385',
                         '2021-02-26': '000037', '2021-01-25': '000069', '2021-02-19': '000044',
                         '2021-02-04': '000059', '2021-02-17': '000047', '2021-01-13': '000081',
                         '2020-03-24': '000383', '2020-04-29': '000345', '2021-02-02': '000061',
                         '2021-03-12': '000023', '2020-04-09': '000366', '2021-02-21': '000042',
                         '2020-05-18': '000326', '2021-02-03': '000060', '2020-03-26': '000380',
                         '2021-02-24': '000039', '2020-05-27': '000317', '2020-06-19': '000294',
                         '2020-05-11': '000333'}


DATE_TO_COLUMN_ID_RSI = {'2021-04-20': '000046', '2021-04-08': '000059', '2021-04-21': '000045',
                         '2021-04-11': '000056', '2021-04-07': '000060', '2021-04-01': '000066',
                         '2021-04-03': '000064', '2021-04-04': '000063', '2021-04-17': '000049',
                         '2021-04-18': '000048', '2021-04-12': '000055', '2021-04-16': '000050',
                         '2021-04-19': '000047', '2021-04-09': '000058', '2021-04-10': '000057',
                         '2021-04-06': '000061', '2021-04-15': '000051', '2021-04-05': '000062',
                         '2021-04-13': '000054', '2021-04-02': '000065'}


DATE_TO_COLUMN_ID_RTS = {'2021-05-11': '000006', '2021-05-01': '000016', '2021-05-09': '000008',
                         '2021-04-27': '000020', '2021-05-07': '000010', '2021-04-26': '000021',
                         '2021-05-10': '000007', '2021-04-30': '000017', '2021-04-23': '000024',
                         '2021-05-04': '000013', '2021-04-25': '000022', '2021-05-05': '000012',
                         '2021-04-24': '000023', '2021-05-08': '000009', '2021-05-02': '000015'}


SL_MAP = {
    "srf": DATE_TO_COLUMN_ID_SRF,
    "rsi": DATE_TO_COLUMN_ID_RSI,
    "rts": DATE_TO_COLUMN_ID_RTS,
}


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-folder", type=str, required=True,
                        help="Which files to potentially modify.")
    parser.add_argument("--dry-run", type=bool, required=False, default=False,
                        help="Do not actually rename.")

    args = parser.parse_args()

    return args


def is_canonical(filename: str) -> bool:
    """

    :param filename:
    :return:
    """
    parts = filename.split(".")
    prefix = parts[0]

    if prefix not in ["srf", "rts", "rsi", "bobsl", "dgs"]:
        return False

    return True


def collect_from_folder(folder_path: str) -> Set[str]:
    """

    :param folder_path:
    :return:
    """
    filepaths = set()

    for filename in os.listdir(folder_path):

        filepath = os.path.join(folder_path, filename)

        filepaths.add(filepath)

    return filepaths


def insert_column_in_filename(filename: str) -> str:
    """
    Example: srf.2016-09-01.srt

    :param filename:
    :return:
    """
    assert is_canonical(filename)

    parts = filename.split(".")

    prefix = parts[0]
    date = parts[1]

    column_id = SL_MAP[prefix][date]

    parts.insert(1, column_id)

    return ".".join(parts)


def rename_file(filepath: str, input_folder: str, dry_run: bool = True):
    """

    :param filepath:
    :param input_folder:
    :param dry_run:
    :return:
    """

    filename = os.path.basename(filepath)

    new_filename = insert_column_in_filename(filename)
    new_filepath = os.path.join(input_folder, new_filename)

    logging.debug("%s -> %s" % (filepath, new_filepath))

    if not dry_run:
        os.rename(filepath, new_filepath)


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)

    paths = collect_from_folder(folder_path=args.input_folder)

    for path in paths:
        rename_file(path, input_folder=args.input_folder, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
