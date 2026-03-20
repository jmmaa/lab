import time
import cv2


FRAMES_DIRECTORY = "./frames"


if __name__ == "__main__":
    video = cv2.VideoCapture("./bad_apple.mp4")

    success, frame = video.read()

    count = 0
    while success:
        height, width, layers = frame.shape

        count += 1

        file = f"{FRAMES_DIRECTORY}/{count}.jpg"
        cv2.imwrite(file, frame)

        time.sleep(0.1)

        print(f"getting {file}")
        success, frame = video.read()

    cv2.destroyAllWindows()
    video.release()
