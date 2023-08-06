import argparse
import dataclasses
import os
from argparse import Namespace
from enum import Enum
from pathlib import Path

import cv2

from img_to_text_converter import ImageToTextConverter, GreyscaleVariants
from progress_bar import DivideProgressBar
from text_video_player import TextVideoPlayer
from youtube_downloader import YoutubeDownloader, Video

subway_video: Video = Video("subway", "https://www.youtube.com/watch?v=uCNR0tKdAVw&ab_channel=SubwaySurfers")
family_guy_video: Video = Video("family", "https://www.youtube.com/watch?v=z5dekcBMYQs&ab_channel=LenoksRecordings")
videos = [
    subway_video,
    family_guy_video,
]

videos_folder = "../videos/"
videos_folder_downloads = videos_folder + "downloads"
videos_folder_processed = videos_folder + "processed"

# description = "A little tool to show subway surfers, family guy funny moments and other entertaining clips in console"
description = "Malý nástroj na přehrávání vtipných momentů z Griffinových, Subway Surfers a jiných zábavných videí v konzoli"


def main() -> None:
    args = initialize_parser()

    clear()
    if not os.path.exists(videos_folder_downloads):
        print("Stahuji videa...")
        os.makedirs(videos_folder_downloads)
        YoutubeDownloader().download_videos(videos, videos_folder_downloads)

    if not os.path.exists(videos_folder_processed):
        os.makedirs(videos_folder_processed)
        process_videos()
    play_text_video(args.type, args.repeat)


def initialize_parser() -> Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--type", help="Druh videa pro přehrání", type=TypeArg, choices=list(TypeArg),
                        default=TypeArg.subway)
    parser.add_argument("-r", "--repeat", help="Přehrávat ve smyčce", action=argparse.BooleanOptionalAction,
                        default=False)
    args = parser.parse_args()
    return args


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


class TypeArg(Enum):
    subway = "subway"
    family = "family"

    def __str__(self):
        return self.value


def process_videos() -> None:
    videos_in_directory = Path(videos_folder_downloads).glob('**/*.mp4')
    for video_path_object in videos_in_directory:
        filename = remove_extension(video_path_object.name)
        filepath_with_filename = str(video_path_object)
        process_video(filepath_with_filename, filename)


def remove_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def process_video(input_path: str, filename: str) -> None:
    save_directory = videos_folder_processed + "/" + filename
    if os.path.exists(save_directory):
        return
    os.makedirs(save_directory)

    video_capture = cv2.VideoCapture(input_path)
    # video_capture.get(cv2.CAP_PROP_FPS)  # TODO save this alongside the video or smth
    success = True
    i = 0
    dimensions = (int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    converter = ImageToTextConverter(dimensions)

    frame_count = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    progress_bar = DivideProgressBar(f"Zpracovávám {filename}", int(frame_count))
    while success:
        success, image = video_capture.read()

        saved_file_path = save_directory + f"/{i + 1}.txt"
        with open(saved_file_path, "w") as file_output:
            file_output.write(converter.img_to_text(image))
            progress_bar.progress(i)
        file_output.close()
        i += 1
    print("")


def play_text_video(video_type: TypeArg, repeat: bool) -> None:
    processed_videos = os.listdir(videos_folder_processed)
    video_to_play = processed_videos[processed_videos.index(get_video_filename(video_type))]

    text_frames: list[str] = []
    path = os.path.join(videos_folder_processed, video_to_play)
    dir_files = os.listdir(path)
    dir_files.sort(key=file_sort)
    for text_frame in dir_files:
        with open(path + "/" + text_frame, "r") as r:
            text_frames.append(r.read())
    text_video_player = TextVideoPlayer(text_frames)
    if not repeat:
        text_video_player.play()
        return

    while True:
        text_video_player.play()


def get_video_filename(video_type: TypeArg):
    if video_type == TypeArg.subway:
        return subway_video.name
    elif video_type == TypeArg.family:
        return family_guy_video.name
    else:
        return subway_video.name


def file_sort(filename: str) -> int:
    return int(filename[:filename.rfind(".")])


if __name__ == '__main__':
    main()
