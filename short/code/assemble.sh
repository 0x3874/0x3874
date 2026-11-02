#!/bin/bash
# frames (540x960 Eevee renders) -> Lanczos to 1080x1920, captions overlay, mixed audio -> H.264/AAC
set -e; cd "$(dirname "$0")/.."
python3 code/captions.py
ffmpeg -y -framerate 30 -start_number 0 -i build/frames/f_%04d.png -f concat -safe 0 -i build/caps.txt -i build/final_audio.wav \
 -filter_complex "[0:v]scale=1080:1920:flags=lanczos,format=rgba[v];[1:v]fps=30,format=rgba[c];[v][c]overlay=0:0:format=auto,format=yuv420p[o]" \
 -map "[o]" -map 2:a -c:v libx264 -preset slow -crf 17 -maxrate 6M -bufsize 12M -r 30 -c:a aac -b:a 256k -shortest -movflags +faststart ${1:-build/short.mp4}
