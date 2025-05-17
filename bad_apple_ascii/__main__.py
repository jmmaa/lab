import os
import soundfile as sf
import sounddevice as sd
import threading

import io
import sys
import time



ascii_frames = os.listdir("ascii_frames")
sorted_ascii_frames = sorted(ascii_frames, key=lambda name: int(name[:name.index(".")]))

loaded_ascii_frames = []



def progress(curr: int, max: int):

    percentage = (curr/max) * 100

    return int(percentage)

count = 0

for ascii_frame in sorted_ascii_frames:
    with open("./ascii_frames/" + ascii_frame, "r") as f:
        
        loaded_ascii_frames.append(f.read())

        count += 1


    print("\033[K", end="\r")
    print("progress (reading frames)", progress(count, len(sorted_ascii_frames)), "%", flush=True, end='')





print("\n")
input("press anything to start")

event = threading.Event()
data, fs = sf.read("bad_apple.wav", always_2d=True)

current_frame = 0

def callback(outdata, frames, time, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(data) - current_frame, frames)
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]
    if chunksize < frames:
        outdata[chunksize:] = 0
        raise sd.CallbackStop()
    current_frame += chunksize






stream = sd.OutputStream(
    samplerate=fs, device=6, channels=data.shape[1],
    callback=callback, finished_callback=event.set)


sys.stdout = open(1, "w", buffering=1)






with stream:
    while stream.active:
        captured_frame = current_frame
        if captured_frame % 1470 >= 334:
            sys.stdout.write('\033[?25l\033[H')
            sys.stdout.write(loaded_ascii_frames[captured_frame//1470])
            sys.stdout.flush()



