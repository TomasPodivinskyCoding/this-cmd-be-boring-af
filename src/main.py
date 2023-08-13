import os
import signal
import sys

import cv2

from args import initialize_parser, TypeArg
from img_to_text_converter import ImageToTextConverter, GreyscaleVariants
from path_getter import get_resources_folder
from progress_bar import DivideProgressBar
from text_video_player import TextVideoPlayer
from youtube_downloader import Video, download_youtube_video

# To add (don't really have the time to create an issue tracker for this)
# Get more zoomer funny distraction videos
# Progress bar when processing video frame for playing (good for longer video)
# More greyscale variants

# PUBLISH TO PYPI
# README

# Print colors in the video
# Allow users to play their own videos

subway_video: Video = Video(
    TypeArg.SUBWAY_SURFERS.value,
    "https://www.youtube.com/watch?v=uCNR0tKdAVw&ab_channel=SubwaySurfers"
)
family_guy_video: Video = Video(
    TypeArg.FAMILY_GUY.value,
    "https://www.youtube.com/watch?v=ppyBo0UfgBk&ab_channel=LenoksRecordings"
)

VIDEOS_FOLDER = get_resources_folder() + "/videos/"
VIDEOS_FOLDER_DOWNLOADS = VIDEOS_FOLDER + "downloads"
VIDEOS_FOLDER_PROCESSED = VIDEOS_FOLDER + "processed"


def main() -> None:
    args = initialize_parser()
    video = get_video_by_type(args.type)

    downloaded_video_filename = f"{video.name}.mp4"
    downloaded_video_path = VIDEOS_FOLDER_DOWNLOADS + "/" + downloaded_video_filename
    if not os.path.exists(downloaded_video_path):
        handle_video_not_downloaded(video)

    greyscale_type_name = args.greyscale_chars.name.lower()
    processed_videos_folder = f"{VIDEOS_FOLDER_PROCESSED}/{video.name}/{greyscale_type_name}"
    if not os.path.exists(processed_videos_folder):
        os.makedirs(processed_videos_folder)
        process_video(
            downloaded_video_path,
            processed_videos_folder,
            video.name,
            args.greyscale_chars
        )
    play_text_video(processed_videos_folder, args.repeat)


def get_video_by_type(type_arg: TypeArg) -> Video:
    if type_arg == TypeArg.SUBWAY_SURFERS:
        return subway_video
    if type_arg == TypeArg.FAMILY_GUY:
        return family_guy_video
    return subway_video


def handle_video_not_downloaded(video: Video) -> None:
    print(f"Stahuji video {video.name}")
    if not os.path.exists(VIDEOS_FOLDER_DOWNLOADS):
        os.makedirs(VIDEOS_FOLDER_DOWNLOADS)
    if not download_youtube_video(
        video.url,
        VIDEOS_FOLDER_DOWNLOADS,
        f"{video.name}.mp4"
    ):
        sys.exit(1)


def process_video(
        input_path: str,
        output_path: str,
        filename: str,
        greyscale_type: GreyscaleVariants
) -> None:
    video_capture = cv2.VideoCapture(input_path)
    dimensions = (
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    )
    converter = ImageToTextConverter(dimensions, greyscale_characters=greyscale_type)

    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = DivideProgressBar(f"Zpracovávám {filename}", frame_count)
    for i in range(int(frame_count)):
        _, image = video_capture.read()

        saved_file_path = output_path + f"/{i + 1}.txt"
        with open(saved_file_path, "w", encoding="UTF-8") as file_output:
            file_output.write(converter.img_to_text(image))
            progress_bar.progress(i + 1)
        file_output.close()
    print("")
    video_capture.release()


def play_text_video(input_path: str, repeat: bool) -> None:
    clear()
    text_frames = load_text_frames(input_path)
    if len(text_frames) == 0:
        print(f"Nebyly nalezeny žádné textové soubory ve složce {input_path}")
        sys.exit(1)

    text_video_player = TextVideoPlayer(text_frames)

    setup_ctrl_c_handler(text_video_player)

    if repeat:
        while True:
            text_video_player.play()
            clear()
    else:
        text_video_player.play()


def load_text_frames(input_path: str) -> list[str]:
    text_frames: list[str] = []
    dir_files = extract_correct_text_files(input_path)
    for text_frame in dir_files:
        with open(input_path + "/" + text_frame, "r", encoding="UTF-8") as opened_text_frame:
            text_frames.append(opened_text_frame.read())
        opened_text_frame.close()
    return text_frames


def extract_correct_text_files(input_path: str) -> list[str]:
    dir_files = os.listdir(input_path)
    dir_files = list(
        filter(lambda file: file.endswith(".txt") and file[:-4].isdigit(), dir_files)
    )

    dir_files.sort(key=file_sort)
    return dir_files


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def setup_ctrl_c_handler(text_video_player: TextVideoPlayer) -> None:
    def handle_ctrl_c(_sig, _frame) -> None:
        print("\n" * text_video_player.new_lines_number)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_ctrl_c)


def file_sort(filename: str) -> int:
    try:
        return int(filename[:filename.rfind(".")])
    except ValueError:
        return 0


if __name__ == '__main__':
    main()
