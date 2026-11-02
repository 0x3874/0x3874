"""One ElevenLabs take (eleven_multilingual_v2, premade Adam) for a story folder. Usage: tts_story.py STORYDIR"""
import json, os, sys, urllib.request, urllib.error, subprocess
S=os.path.abspath(sys.argv[1]); text="\n".join(l.strip() for l in open(S+"/script_lines.txt") if l.strip())
env=dict(l.strip().split("=",1) for l in open(os.environ["ENV_FILE"]) if "=" in l)
body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.55,"similarity_boost":0.8,"style":0.25}}).encode()
r=urllib.request.Request("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB?output_format=mp3_44100_128",body,{"xi-api-key":env["ELEVENLABS_API_KEY"],"Content-Type":"application/json"})
try: d=urllib.request.urlopen(r,timeout=180).read()
except urllib.error.HTTPError as e: sys.exit(f"HTTP {e.code}: {e.read().decode()[:300]}")
open(S+"/voice_raw.mp3","wb").write(d); print("ok",len(d),"bytes,",len(text),"characters")
subprocess.run(["ffmpeg","-v","error","-y","-i",S+"/voice_raw.mp3","-ar","44100","-ac","1",S+"/voice_raw.wav"],check=True)
