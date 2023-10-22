import osrparse as os
import sys
import ffmpeg
import tempfile
from PIL import Image, ImageDraw 

WIDTH = 100                 # WIDTH OF VIDEO
HEIGHT = 400                # HEIGHT OF VIDEO
FPS = 60                    # FRAMERATE OF VIDEO
KEYWIDTH = 30               # WIDTH OF KEYS IN PIXELS
SEGMENTS = 100              # AMOUNT OF SEGMENTS IN HEIGHT (BLOCKS MOVE ONE SEGMENT EACH FRAME)
COLOR = "#FFFFFF"           # COLOR OF THE BLOCKS

DELTA_TIME = 1000/FPS
PADDING = (WIDTH - 2*KEYWIDTH) / 3
FRAMEHEIGHT = HEIGHT/SEGMENTS
K1POS = PADDING
K2POS = 2*PADDING + KEYWIDTH

def drawFrame(frame, s1, s2):
    img = Image.new("RGB", (WIDTH, HEIGHT)) 
    img1 = ImageDraw.Draw(img)   
    frame_end = frame+SEGMENTS
    
    for seg in s1:
        if seg[1] < frame: continue
        if seg[0] > frame_end: break
        img1.rectangle((K1POS, (max(seg[0], frame)-frame)*FRAMEHEIGHT, K1POS+KEYWIDTH, (min(seg[1], frame_end)-frame)*FRAMEHEIGHT), fill=COLOR)
        
    for seg in s2:
        if seg[1] < frame: continue
        if seg[0] > frame_end: break
        img1.rectangle((K2POS, (max(seg[0], frame)-frame)*FRAMEHEIGHT, K2POS+KEYWIDTH, (min(seg[1], frame_end)-frame)*FRAMEHEIGHT), fill=COLOR)
       
    img.save(f"{tmpdir}/{frame:06d}.jpg", "JPEG")

if len(sys.argv) < 3:
    print("Invalid number of arguments. Usage: python parse.py <replay_path> <output_path>")
    exit()   
    
path_to_replay = str(sys.argv[1])
path_to_output = str(sys.argv[2])

replay = os.Replay.from_path(path_to_replay)

print(f"Reading {str(replay.username)}'s score on beatmap {str(replay.beatmap_hash)}")
print(f'Set on {replay.timestamp:%Y-%m-%d %H:%M:%S%z}')
accuracy = (replay.count_50 * 50 + replay.count_100 * 100 + replay.count_300 * 300) / 300 / (replay.count_miss + replay.count_50 + replay.count_100 + replay.count_300)
print(f"{accuracy*100:.2f}% Accuracy ({str(replay.count_300)}/{str(replay.count_100)}/{str(replay.count_50)}/{str(replay.count_miss)})")

data = replay.replay_data

total_time = 0
events = ([(total_time := event.time_delta + total_time, event.keys) for event in data])

key1_segments = []
key2_segments = []
pressed1 = 0
pressed2 = 0
seg1_begin = 0
seg1_end = 0
seg2_begin = 0
seg2_end = 0

frame = 0
index = 0
while frame*DELTA_TIME <= total_time:
    while events[index][0] <= frame*DELTA_TIME: index += 1

    # Key1
    if events[index][1] & (1 << 2) > 0: 
        if pressed1: seg1_end = frame 
        else: 
            seg1_begin = frame 
            seg1_end = frame 
        pressed1 = 1
    elif pressed1:
        key1_segments.append((seg1_begin + SEGMENTS, seg1_end + SEGMENTS))
        pressed1 = 0
        
    # Key2
    if events[index][1] & (1 << 3) > 0: 
        if pressed2: seg2_end = frame
        else: 
            seg2_begin = frame
            seg2_end = frame
        pressed2 = 1
    elif pressed2:
        key2_segments.append((seg2_begin + SEGMENTS, seg2_end + SEGMENTS))
        pressed2 = 0
       
    frame += 1

with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Drawing Frames to {tmpdir}...")
    for i in range(0, frame): drawFrame(i, key1_segments, key2_segments)

    print("Combining into video...")
    (
        ffmpeg
        .input(f'{tmpdir}/*.jpg', pattern_type='glob', framerate=FPS)
        .output(path_to_output, framerate=FPS)
        .run()
    )   

print("Done!")
