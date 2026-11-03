# Renders and assembles all 7 week-1 Shorts at full quality. Run from the `short` folder:  powershell -ExecutionPolicy Bypass -File .\render_all.ps1
# Needs: Python 3.13 (py -V:3.13) with bpy numpy pillow fonttools, and ffmpeg on PATH. Output: stories\<name>\short.mp4
$stories = @(
  @{ n = "s01_do_not_answer"; f = 1267 }, @{ n = "s02_the_cactus"; f = 1153 }, @{ n = "s03_one_inch"; f = 1466 },
  @{ n = "s04_the_snowman"; f = 1436 }, @{ n = "s05_free_pizza"; f = 1441 }, @{ n = "s06_thirteen"; f = 1454 }, @{ n = "s07_one_percent"; f = 1361 }
)
$env:PCT = 100; $env:SAMPLES = 32
foreach ($s in $stories) {
  $n = $s.n; $env:STORY = $n; Write-Host "=== $n ==="
  py -V:3.13 code\build.py full "stories\$n\frames" 0 $s.f
  py -V:3.13 code\captions.py "stories\$n"
  ffmpeg -y -framerate 30 -i "stories/$n/frames/f_%04d.png" -f concat -safe 0 -i "stories/$n/caps.txt" -i "stories/$n/final_audio.wav" `
    -filter_complex "[0:v]scale=1080:1920:flags=lanczos,format=rgba[v];[1:v]fps=30,format=rgba[c];[v][c]overlay=0:0:format=auto,format=yuv420p[o]" `
    -map "[o]" -map 2:a -c:v libx264 -preset slow -crf 17 -maxrate 6M -bufsize 12M -r 30 -c:a aac -b:a 256k -shortest "stories/$n/short.mp4"
}
