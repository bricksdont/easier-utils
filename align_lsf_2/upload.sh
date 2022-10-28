#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

via=$base/via
csv=$base/csv

data=/net/cephfs/scratch/mathmu/align_lsf_2

# upload videos

scp $data/videos_mp4/*.mp4 mmueller@login.cl.uzh.ch:/mnt/storage/clfiles/users/mmueller/www/easier/via/

# upload VIA json

python $base/align_lsf_2/srt2via.py -i $csv/align_lsf_2.csv -o $via/align_lsf_2.json
