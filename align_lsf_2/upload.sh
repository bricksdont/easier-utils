#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/net/cephfs/scratch/mathmu/align_lsf_2

via=$data/via

# upload videos

scp $data/videos_mp4/*.mp4 mmueller@login.cl.uzh.ch:/mnt/storage/clfiles/users/mmueller/www/easier/via/

# upload VIA jsons ?
