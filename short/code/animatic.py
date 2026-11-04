"""Quick preview ("animatic"): the per-shot still images held for their shot length + captions + final audio -> previews/<story>.mp4 (540x960)."""
import glob, json, os, re, subprocess, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")) + "/"
S = os.path.abspath(sys.argv[1]) + "/"; name = os.path.basename(S.rstrip("/"))
d = S + "stills_v2" if os.path.isdir(S + "stills_v2") else S + "stills"
fs = sorted(glob.glob(d + "/s*_f*.png")); mids = [int(re.search(r"_f(\d+)\.png", f).group(1)) for f in fs]
tm = json.load(open(S + "timing.json")); END = tm["END_T"] * 30
bounds = [0] + [(a + b) / 2 for a, b in zip(mids, mids[1:])] + [END]
lines = ["ffconcat version 1.0"]
for f, a, b in zip(fs, bounds, bounds[1:]): lines += [f"file {f}", f"duration {(b - a) / 30:.4f}"]
lines.append(f"file {fs[-1]}")
open(S + "animatic.txt", "w").write("\n".join(lines) + "\n")
out = R + f"previews/{name}.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", S + "animatic.txt", "-f", "concat", "-safe", "0", "-i", S + "caps.txt", "-i", S + "final_audio.wav",
    "-filter_complex", "[0:v]fps=30,scale=540:960,format=rgba[v];[1:v]fps=30,scale=540:960,format=rgba[c];[v][c]overlay=0:0:format=auto,format=yuv420p[o]",
    "-map", "[o]", "-map", "2:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "128k", "-shortest", out], check=True)
print(out, round(os.path.getsize(out) / 1e6, 1), "MB")
