#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

data=/scratch/mathmu/align_lis

via=$data/via

# upload videos

scp $data/videos_mp4/*.mp4 mmueller@login.cl.uzh.ch:/mnt/storage/clfiles/users/mmueller/www/easier/via/

# upload VIA jsons ?
