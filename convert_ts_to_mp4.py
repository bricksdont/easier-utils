#! /usr/bin/python3

"""
Will fix date formats and optionally preprend a prefix string to a filename.
"""

import os
import argparse
import logging
import subprocess

from typing import Tuple

# fix malformed audio bitstream (expected if converting TS to MP4):
# ffmpeg -i input.ts -c:v libx264 -crf 18 -c:a copy -bsf:a aac_adtstoasc output.mp4
#
# OR re-encode audio as well:
# ffmpeg -i input.ts -c:v libx264 -crf 18 -strict -2 -c:a aac output.mp4

FFMPEG_TEMPLATE = "ffmpeg -y -threads {num_threads} -i {input_path} -crf {crf} -c:v libx264 -c:a copy -bsf:a aac_adtstoasc {output_path}"


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str,
                        help="Absolute path to input file.", required=True)
    parser.add_argument("--output", type=str,
                        help="Absolute path to output file.", required=True)

    parser.add_argument("--ffmpeg-multithreaded", action="store_true",
                        help="Use all threads for ffmpeg.", required=False)

    parser.add_argument("--ffmpeg-crf", type=int, default=18,
                        help="H.264 encoding constant rate factor (CRF), 18 considered visually lossless.", required=False)

    args = parser.parse_args()

    return args


def convert_video(input_path: str,
                  output_path: str,
                  multithreaded: bool,
                  crf: int = 18) -> Tuple[str, str]:
    """

    :param input_path:
    :param output_path:
    :param multithreaded:
    :param crf:
    :return:
    """

    if os.path.exists(output_path):
        logging.debug("Converted video file exists, will skip calling ffmpeg: '%s'" % output_path)
        return "", ""

    logging.debug("Writing file: %s" % output_path)

    if multithreaded:
        num_threads = "auto"
    else:
        num_threads = "1"

    ffmpeg_cmd = FFMPEG_TEMPLATE.format(input_path=input_path,
                                        output_path=output_path,
                                        crf=crf,
                                        num_threads=num_threads)

    logging.debug("Executing:")
    logging.debug(ffmpeg_cmd)

    result = subprocess.run(ffmpeg_cmd, shell=True, capture_output=True)

    return result.stdout.decode("utf-8"), result.stderr.decode("utf-8")


def main():

    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)

    convert_video(input_path=args.input, output_path=args.output, multithreaded=args.ffmpeg_multithreaded,
                  crf=args.ffmpeg_crf)


if __name__ == '__main__':
    main()
