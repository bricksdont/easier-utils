#! /usr/bin/python3

"""
Statistics about subtitle directory.
"""

import os
import srt
import argparse
import logging

import numpy as np

from typing import List


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", type=str,
                        help="Folder with srt files.", required=True)

    args = parser.parse_args()

    return args


def get_duration(subtitle: srt.Subtitle) -> float:
    """

    :param subtitle:
    :return:
    """

    duration = subtitle.end - subtitle.start

    return float(duration.total_seconds())


def get_average_duration(subtitles: List[srt.Subtitle]) -> float:

    durations = []

    for subtitle in subtitles:
        duration = get_duration(subtitle)
        durations.append(duration)

    return float(np.mean(durations))


def read_srt(filepath: str) -> List[srt.Subtitle]:
    """

    :param filepath:
    :return:
    """
    subtitles = []

    with open(filepath, "r") as handle:
        for subtitle in srt.parse(handle.read()):

            if subtitle.content.strip() == "":
                continue

            subtitles.append(subtitle)

    return subtitles


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

    subtitle_stats = []

    for filename in os.listdir(args.folder):

        filepath = os.path.join(args.folder, filename)

        subtitles = read_srt(filepath)

        num = len(subtitles)

        average_duration = get_average_duration(subtitles)

        subtitle_stats.append({"filename": filename,
                               "num": num,
                               "filepath": filepath,
                               "average_duration": average_duration})

    subtitle_stats_sorted = sorted(subtitle_stats, key=lambda d: d['num'])

    for stat in subtitle_stats_sorted:
        print(stat)


if __name__ == '__main__':
    main()
