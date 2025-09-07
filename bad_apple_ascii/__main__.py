import os
import sys
import threading
import time
import asyncio
import aiofiles

import soundfile as sf
import sounddevice as sd


current_frame = 0


async def main():
    loaded_ascii_frames_dict = {}

    tasks = []

    start_loading_frames_time = time.time()

    file = "bad_apple.wav"

    print("\033[?25l\033[H\033[2Jloading frames...")

    ascii_frames = os.listdir("ascii_frames")
    sorted_ascii_frames = sorted(
        ascii_frames, key=lambda name: int(name[: name.index(".")])
    )

    async def read_ascii_frame_async(ascii_frame: str):
        async with aiofiles.open("./ascii_frames/" + ascii_frame, "r") as f:
            data = await f.read()

            n = int(ascii_frame.replace(".txt", ""))
            loaded_ascii_frames_dict[n] = data

    for ascii_frame in sorted_ascii_frames:
        tasks.append(read_ascii_frame_async(ascii_frame))

    await asyncio.gather(*tasks)

    print("loaded frames (%.2fs)" % (time.time() - start_loading_frames_time))
    loaded_ascii_frames = [
        value[1]
        for value in sorted(loaded_ascii_frames_dict.items(), key=lambda e: e[0])
    ]

    input("\npress anything to start")

    event = threading.Event()
    data, fs = sf.read(file, always_2d=True)

    def callback(outdata, frames, time, status):
        global current_frame
        if status:
            print(status)
        chunksize = min(len(data) - current_frame, frames)
        outdata[:chunksize] = data[current_frame : current_frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            raise sd.CallbackStop()
        current_frame += chunksize

    stream = sd.OutputStream(
        samplerate=fs,
        device=5,
        channels=data.shape[1],
        callback=callback,
        finished_callback=event.set,
    )

    sys.stdout = open(1, "w", buffering=1)

    with stream:
        while stream.active:
            captured_frame = current_frame

            seconds = captured_frame // fs

            frame_val = captured_frame // (fs // 30)

            sys.stdout.write("\033[?25l\033[H")
            sys.stdout.write(loaded_ascii_frames[frame_val])
            sys.stdout.write(
                f"\n\nfile: {file}\t\tframes per second: {0 if seconds == 0 else frame_val // seconds}"
            )
            sys.stdout.write(f"\nframe: {frame_val}\t\t\tduration: {seconds}s")
            sys.stdout.flush()


asyncio.run(main())
