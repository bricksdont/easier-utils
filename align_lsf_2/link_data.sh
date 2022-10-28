#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

origin=/net/cephfs/shares/volk.cl.uzh/EASIER/WP4/spoken-to-sign_sign-to-spoken/LSF-CH/RTS/Daily_news
target=/net/cephfs/scratch/mathmu/align_lsf_2

eval "$(conda shell.bash hook)"
source activate /net/cephfs/shares/volk.cl.uzh/EASIER/WMT_Shared_Task/processing-shared-task-data/venvs/venv

# sets variable: file_ids

. $base/align_lsf_2/define_ids.sh

# videos

origin_sub=$origin/videos/videos_parallel
target_sub=$target/videos_ts

for file_id in $file_ids; do
    ln -s $origin_sub/rts.$file_id.ts $target_sub/rts.$file_id.ts
done

# subtitles

origin_sub=$origin/subtitles/subtitles_parallel
target_sub=$target/subtitles_srt

for file_id in $file_ids; do
    ln -s $origin_sub/rts.$file_id.srt $target_sub/rts.$file_id.srt
done
