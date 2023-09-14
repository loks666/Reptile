import os
import cv2


def check_video_audio(video_path):
    vid = cv2.VideoCapture(video_path)
    has_audio = False

    if vid.isOpened():
        _, frame = vid.read()
        if frame is not None:
            channels = frame.shape[2] if len(frame.shape) == 3 else 1
            if channels > 1:
                has_audio = True

    vid.release()
    return has_audio


def main():
    folder_path = r"E:\group\MP4\test"
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]

    for file in video_files:
        video_path = os.path.join(folder_path, file)
        if check_video_audio(video_path):
            print(f"The video '{file}' has audio.")
        else:
            print(f"The video '{file}' does not have audio.")


if __name__ == "__main__":
    main()
    exit(0)
