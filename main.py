import os
from pathlib import Path

import cv2

from img_to_text_converter import ImageToTextConverter
from youtube_downloader import download_videos

videos_folder = "./subway_surfers_videos"
videos_folder_downloads = videos_folder + "/downloads"
videos_folder_frames = videos_folder + "/frames"
videos_folder_processed = videos_folder + "/processed"

subway_surfers_gameplay_videos = [
    "https://www.youtube.com/watch?v=_Z5hxyn3COw&ab_channel=mozzik07"
]


def download_video_frames() -> None:
    videos_in_directory = Path(videos_folder_downloads).glob('**/*.mp4')
    for video_path_object in videos_in_directory:
        filename = remove_extension(video_path_object.name)
        filepath_with_filename = str(video_path_object)
        processed_file_folder = videos_folder_frames + "/" + filename
        if not os.path.exists(processed_file_folder):
            os.makedirs(processed_file_folder)
            video_to_frames(filepath_with_filename, processed_file_folder)


def remove_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]


def video_to_frames(input_path: str, output_path: str) -> None:
    # https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
    frame_count = 1
    video_capture = cv2.VideoCapture(input_path)
    success = True
    i = 0
    max_frames_saved = 100
    while success and i < max_frames_saved:
        video_capture.set(cv2.CAP_PROP_POS_MSEC, (frame_count * 1000))  # TODO the fuck this line does?
        success, image = video_capture.read()
        # TODO this may be retarded. I could just stream the files instead of saving em
        cv2.imwrite(output_path + "/frame%d.jpg" % frame_count, image)  # save frame as JPEG file
        frame_count = frame_count + 1
        i += 1


def process_video_frames() -> None:
    for directory in os.listdir(videos_folder_frames):
        saved_frames_dir = videos_folder_processed + "/" + directory
        if not os.path.exists(saved_frames_dir):
            os.makedirs(saved_frames_dir)

        converter = ImageToTextConverter()
        current_video_frames_directory = Path(videos_folder_frames + "/" + directory).glob('**/*.jpg')
        for video_path_object in current_video_frames_directory:
            input_frame_path = f".\\{str(video_path_object)}"
            output_frame_path = videos_folder_processed + "/" + directory + "/" + remove_extension(
                video_path_object.name) + ".txt"
            with open(output_frame_path, "w") as file_output:
                file_output.write(converter.img_to_text(input_frame_path))
            file_output.close()


if __name__ == '__main__':
    if not os.path.exists(videos_folder_downloads):
        os.makedirs(videos_folder_downloads)
        download_videos(subway_surfers_gameplay_videos, videos_folder_downloads)

    if not os.path.exists(videos_folder_processed):
        os.makedirs(videos_folder_processed)

    if not os.path.exists(videos_folder_frames):
        os.makedirs(videos_folder_frames)

    download_video_frames()
    process_video_frames()
