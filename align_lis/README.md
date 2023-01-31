## Prepare LIS data for first round of human alignment

First canonicalize dates and prefix with “rts”. To test the renaming without actually executing it:

    for filepath in /shares/easier.volk.cl.uzh/WP4/spoken-to-sign_sign-to-spoken/LIS-CH/RSI/Daily_news/videos/videos_parallel/*.ts;
        do python3 ../canonicalize_date.py --input $filepath --dry-run --prefix "rsi."; done

After that, remove the `--dry-run` argument to actually rename the files.

Link data, run:

    ./link_data.sh

Convert ts videos to mp4, run:

    ./submit_convert_videos.sh

Convert srt subtitles to via, run:

    ./create_via_csv.sh
    ./create_via_json.sh

and upload everything:

    ./upload.sh

The VIA files will then be available here:

https://pub.cl.uzh.ch/projects/easier/via/

## Tips

Check all videos to make sure they are regular daily news episodes.

Check all subtitle files (e.g. using the script in this repo called `srt_stats.py`) to make sure the number of
subtitles is reasonable.

Open one resulting VIA project to make sure videos and subtitles are correctly paired together, and
audio and subtitles roughly match.

## License of SRT2VIA script

`src2via.py` was developed by Marco Giovanelli.

This script is released as Open Source according to the "2-Clause BSD License":

```
Copyright (c) 2020, developed by Marco Giovanelli for FINCONS GROUP AG
within the CONTENT4ALL Project.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```
