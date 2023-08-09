import os
from pathlib import Path

import cv2

from args import initialize_parser, TypeArg
from img_to_text_converter import ImageToTextConverter
from progress_bar import DivideProgressBar
from text_video_player import TextVideoPlayer
from youtube_downloader import YoutubeDownloader, Video

# To add (don't really have the time to create an issue tracker for this)
# Print colors in the video
# Allow users to play their own videos
# React to ctrl+c and clear the console
# Progress bar when processing video frame for playing
# Get more videos
# Fix clear with repeat flag
# README
# PUBLISH TO PYPI

subway_video: Video = Video(
    TypeArg.SUBWAY_SURFERS.value,
    "https://www.youtube.com/watch?v=uCNR0tKdAVw&ab_channel=SubwaySurfers"
)
family_guy_video: Video = Video(
    TypeArg.FAMILY_GUY.value,
    "https://www.youtube.com/watch?v=z5dekcBMYQs&ab_channel=LenoksRecordings"
)

VIDEOS_FOLDER = "../videos/"
VIDEOS_FOLDER_DOWNLOADS = VIDEOS_FOLDER + "downloads"
VIDEOS_FOLDER_PROCESSED = VIDEOS_FOLDER + "processed"


def main() -> None:
    args = initialize_parser()
    video = get_video_by_type(args.type)

    downloaded_video_filename = f"{video.name}.mp4"
    downloaded_video_path = VIDEOS_FOLDER_DOWNLOADS + "/" + downloaded_video_filename
    if not os.path.exists(downloaded_video_path):
        print(f"Stahuji video {video.name}")
        os.makedirs(VIDEOS_FOLDER_DOWNLOADS)
        YoutubeDownloader().download_youtube_video(
            video.url,
            VIDEOS_FOLDER_DOWNLOADS,
            f"{video.name}.mp4"
        )

    processed_videos_folder = VIDEOS_FOLDER_PROCESSED + "/" + video.name
    if not os.path.exists(processed_videos_folder):
        os.makedirs(processed_videos_folder)
        process_video(downloaded_video_path, processed_videos_folder, video.name)

    play_text_video(args.type, args.repeat)


def get_video_by_type(type_arg: TypeArg) -> Video:
    if type_arg == TypeArg.SUBWAY_SURFERS:
        return subway_video
    elif type_arg == TypeArg.FAMILY_GUY:
        return family_guy_video
    else:
        raise Exception("Unknown video type")


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def process_videos() -> None:
    videos_in_directory = Path(VIDEOS_FOLDER_DOWNLOADS).glob('**/*.mp4')
    for video_path_object in videos_in_directory:
        filename = remove_extension(video_path_object.name)
        filepath_with_filename = str(video_path_object)
        process_video(filepath_with_filename, filename)


def remove_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def process_video(input_path: str, output_path: str, filename: str) -> None:
    video_capture = cv2.VideoCapture(input_path)
    dimensions = (
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    )
    converter = ImageToTextConverter(dimensions)

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


def play_text_video(video_type: TypeArg, repeat: bool) -> None:
    processed_videos = os.listdir(VIDEOS_FOLDER_PROCESSED)
    video_to_play = processed_videos[processed_videos.index(get_video_filename(video_type))]

    text_frames: list[str] = []
    path = os.path.join(VIDEOS_FOLDER_PROCESSED, video_to_play)
    dir_files = os.listdir(path)
    dir_files.sort(key=file_sort)
    for text_frame in dir_files:
        with open(path + "/" + text_frame, "r", encoding="UTF-8") as opened_text_frame:
            text_frames.append(opened_text_frame.read())

    clear()

    text_video_player = TextVideoPlayer(text_frames)
    if not repeat:
        text_video_player.play()
        return

    while True:
        text_video_player.play()


def get_video_filename(video_type: TypeArg):
    if video_type == TypeArg.SUBWAY_SURFERS:
        return subway_video.name
    if video_type == TypeArg.FAMILY_GUY:
        return family_guy_video.name
    return subway_video.name


def file_sort(filename: str) -> int:
    return int(filename[:filename.rfind(".")])


if __name__ == '__main__':
    main()
