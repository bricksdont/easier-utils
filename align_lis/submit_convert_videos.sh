#! /bin/bash

module load anaconda3

base=$(dirname "$0")/..
base=$(realpath $base)

# sets variable: file_ids

. $base/align_lis/define_ids.sh

logs=$base/align_lis/logs
logs_sub=$logs/convert_videos

mkdir -p $logs
mkdir -p $logs_sub

SLURM_DEFAULT_FILE_PATTERN="slurm-%j.out"
SLURM_LOG_ARGS="-o $logs_sub/$SLURM_DEFAULT_FILE_PATTERN -e $logs_sub/$SLURM_DEFAULT_FILE_PATTERN"

SLURM_ARGS_GENERIC="--cpus-per-task=8 --time=01:00:00 --mem=8G"

for file_id in $file_ids; do
    sbatch \
        $SLURM_ARGS_GENERIC \
        $SLURM_LOG_ARGS \
        $base/align_lis/convert_video.sh \
        $base $file_id
done
