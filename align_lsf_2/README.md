## Prepare LSF data for second round of human alignment

First canonicalize dates and prefix with “rts”.

Run this to test the script:

    python3 canonicalize_date.py --input $filepath --dry-run --prefix "rts."

Link data, run:

    ./link_data.sh

Convert ts videos to mp4, run:

    ./submit_convert_videos.sh

Convert srt subtitles to via, run:

    ./submit_convert_subtitles.sh
