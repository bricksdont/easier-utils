#! /usr/bin/python3

"""
Example:

project_name,video_url,srt_file_path,srt_file_encoding
2021-05-13,https://pub.cl.uzh.ch/projects/easier/dload/2021-05-13.mp4,/Users/.../subtitles/2021-05-13.srt,utf_8
"""

import os
import csv
import sys
import argparse
import logging

from typing import Dict, List


PUBLIC_URL_PREFIX = "https://pub.cl.uzh.ch/projects/easier/via"

CSV_HEADER = ["project_name", "video_url", "srt_file_path", "srt_file_encoding"]


def get_id(filename: str) -> str:
    """

    :param filename:
    :return:
    """
    parts = filename.split(".")

    return parts[1]


def load_files_as_dict(folder_path: str) -> Dict[str, str]:
    """

    :param folder_path:
    :return:
    """
    filepaths_by_id = {}

    for filename in os.listdir(folder_path):
        file_id = get_id(filename)
        filepath = os.path.join(folder_path, filename)

        filepaths_by_id[file_id] = filepath

    return filepaths_by_id


def get_video_url(file_id: str, prefix: str) -> str:
    """

    :param file_id:
    :param prefix:
    :return:
    """

    filename = "%s.%s.mp4" % (prefix, file_id)

    return PUBLIC_URL_PREFIX + "/" + filename


def write_csv_output(rows: List[List[str]]):
    """

    :param rows:
    :return:
    """
    writer = csv.writer(sys.stdout)

    writer.writerow(CSV_HEADER)

    for row in rows:
        writer.writerow(row)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--videos", type=str,
                        help="Absolute path to input folder with videos.", required=True)
    parser.add_argument("--subtitles", type=str,
                        help="Absolute path to input folder with videos.", required=True)
    parser.add_argument("--prefix", type=str,
                        help="File name prefix such as 'rts' or 'rsi'.", required=True)

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)

    video_files = load_files_as_dict(args.videos)
    subtitle_files = load_files_as_dict(args.subtitles)

    rows = []  # type: List[List[str]]

    for file_id, video_filepath in video_files.items():
        subtitle_filepath = subtitle_files[file_id]

        video_url = get_video_url(file_id, prefix=args.prefix)

        # ["project_name", "video_url", "srt_file_path", "srt_file_encoding"]

        row = [file_id, video_url, subtitle_filepath, "utf_8"]

        rows.append(row)

    rows.sort()

    write_csv_output(rows)


if __name__ == '__main__':
    main()
