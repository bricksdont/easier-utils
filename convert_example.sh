#! /bin/bash

eval "$(conda shell.bash hook)"
source activate /shares/easier.volk.cl.uzh/WMT_Shared_Task/processing-shared-task-data/venvs/venv

python $base/convert_ts_to_mp4.py \
   --input /shares/easier.volk.cl.uzh/EASIER/WP4/spoken-to-sign_sign-to-spoken/LSF-CH/RTS/Daily_news/videos/videos_parallel/2021-5-6.ts \
   --output ~/scratch/lsf_align_2/easier-utils/t.mp4 \
   --ffmpeg-multithreaded
