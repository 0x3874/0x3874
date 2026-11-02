#!/bin/bash
# usage: bash code/assemble_story.sh stories/s01_do_not_answer   (frames in <story>/frames/f_0000.png ...)
set -e; cd "$(dirname "$0")/.."; S="${1%/}"
python3 code/captions.py "$S"
ffmpeg -y -framerate 30 -start_number 0 -i "$S/frames/f_%04d.png" -f concat -safe 0 -i "$S/caps.txt" -i "$S/final_audio.wav" \
 -filter_complex "[0:v]scale=1080:1920:flags=lanczos,format=rgba[v];[1:v]fps=30,format=rgba[c];[v][c]overlay=0:0:format=auto,format=yuv420p[o]" \
 -map "[o]" -map 2:a -c:v libx264 -preset slow -crf 17 -maxrate 6M -bufsize 12M -r 30 -c:a aac -b:a 256k -shortest -movflags +faststart "$S/short.mp4"
