import os

import ascii_magic
from create_video_frames import FRAMES_DIRECTORY


ASCII_FRAMES_DIRECTORY = "./ascii_frames"

frames = os.listdir("frames")
sorted_frame_paths = sorted(frames, key=lambda name: int(name[: name.index(".")]))


for frame in frames:
    ascii_frame = ascii_magic.AsciiArt.from_image(f"{FRAMES_DIRECTORY}/{frame}")
    count = int(frame[: frame.index(".")])
    ascii_frame.to_file(
        f"{ASCII_FRAMES_DIRECTORY}/{count}.txt", monochrome=True, columns=120
    )
