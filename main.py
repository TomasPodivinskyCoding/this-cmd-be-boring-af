import os
import re
import time
from pathlib import Path

import cv2

from img_to_text_converter import ImageToTextConverter
from youtube_downloader import download_videos

videos_folder = "./subway_surfers_videos/"
videos_folder_downloads = videos_folder + "downloads"
videos_folder_processed = videos_folder + "processed"

processed_filename = "frame"

subway_surfers_gameplay_videos = [
    "https://www.youtube.com/watch?v=_Z5hxyn3COw&ab_channel=mozzik07"
]

converter = ImageToTextConverter()


def main() -> None:
    if not os.path.exists(videos_folder_downloads):
        os.makedirs(videos_folder_downloads)
        download_videos(subway_surfers_gameplay_videos, videos_folder_downloads)

    if not os.path.exists(videos_folder_processed):
        os.makedirs(videos_folder_processed)

    process_videos()
    play_text_video()


def process_videos() -> None:
    videos_in_directory = Path(videos_folder_downloads).glob('**/*.mp4')
    for video_path_object in videos_in_directory:
        filename = remove_extension(video_path_object.name)
        filepath_with_filename = str(video_path_object)
        process_video(filepath_with_filename, filename)


def remove_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def process_video(input_path: str, filename: str) -> None:
    # https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
    video_capture = cv2.VideoCapture(input_path)
    success = True
    i = 0
    max_frames_processed = 1000
    save_directory = videos_folder_processed + "/" + filename
    if os.path.exists(save_directory):
        return

    os.makedirs(save_directory)

    while success and i < max_frames_processed:
        video_capture.set(cv2.CAP_PROP_POS_MSEC, ((i + 1) * 1000))  # TODO the fuck this line does?
        success, image = video_capture.read()

        saved_file_path = save_directory + f"/{processed_filename}{i + 1}.txt"
        with open(saved_file_path, "w") as file_output:
            file_output.write(converter.img_to_text(image))
            print(f"Zpracováno {saved_file_path}")
        file_output.close()

        i += 1


def play_text_video() -> None:
    text_frames: list[str] = []
    for processed_video_folder in os.listdir(videos_folder_processed):
        path = os.path.join(videos_folder_processed, processed_video_folder)
        if os.path.isdir(path):
            dir_files = os.listdir(path)
            dir_files.sort(key=file_sort)
            for text_frame in dir_files:
                with open(path + "/" + text_frame, "r") as r:
                    text_frames.append(r.read())

    clear_function = get_os_clear_function()

    fps = 24
    delay = 1 / fps
    for text_frame in text_frames:
        os.system(clear_function)
        print(text_frame)
        time.sleep(delay)


def file_sort(f: str) -> int:
    return int(f[len(processed_filename):f.rfind(".")])


def get_os_clear_function() -> str:
    if os.name == 'nt':
        return 'cls'
    return 'clear'


if __name__ == '__main__':
    main()
