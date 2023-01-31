#! /bin/bash

base=$(dirname "$0")/..
base=$(realpath $base)

origin=/shares/easier.volk.cl.uzh/WP4/spoken-to-sign_sign-to-spoken/LIS-CH/RSI/Daily_news
target=/scratch/mathmu/align_lis

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

prefix="rsi"

# sets variable: file_ids

. $base/align_lis/define_ids.sh

# videos

origin_sub=$origin/videos/videos_parallel
target_sub=$target/videos_ts

mkdir -p $target_sub

for file_id in $file_ids; do
    echo "linking: $origin_sub/$prefix.$file_id.ts -> $target_sub/$prefix.$file_id.ts"
    ln -s $origin_sub/$prefix.$file_id.ts $target_sub/$prefix.$file_id.ts
done

# subtitles

origin_sub=$origin/subtitles/subtitles_parallel
target_sub=$target/subtitles

mkdir -p $target_sub

for file_id in $file_ids; do
    echo "linking: $origin_sub/$prefix.$file_id.srt -> $target_sub/$prefix.$file_id.srt"
    ln -s $origin_sub/$prefix.$file_id.srt $target_sub/$prefix.$file_id.srt
done
