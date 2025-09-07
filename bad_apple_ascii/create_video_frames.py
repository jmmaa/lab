import cv2


FRAMES_DIRECTORY = "./frames"


if __name__ == "__main__":
    video = cv2.VideoCapture("bad_apple.mp4")

    success, frame = video.read()
    count = 0
    while success:
        height, width, layers = frame.shape

        count += 1

        cv2.imwrite(f"{FRAMES_DIRECTORY}/{count}.jpg", frame)
        success, frame = video.read()
