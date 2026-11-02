# Render the Short at full quality on a GPU machine
Needs Python 3.11, FFmpeg, and: `pip install bpy==5.2.3 numpy pillow fonttools`
(Windows/Mac: no xvfb needed. Linux with a GPU: run under a normal desktop or `xvfb-run -a`.)

1. Review one frame:   `PCT=50 SAMPLES=12 python code/build.py frame build/stills 640`
2. Full render:        `PCT=100 SAMPLES=32 python code/build.py full build/frames 0 1235`
   (split the range across several terminals to use more GPUs/cores; frames are named build/frames/f_0000.png ...)
3. Assemble:           `bash code/assemble.sh build/short.mp4`
Audio (`build/final_audio.wav`) is already built and committed; assemble.sh rebuilds the caption PNGs for your paths. The scale step is harmless on 1080x1920 frames.
