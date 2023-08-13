import dataclasses

import pytube.exceptions
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from progress_bar import BlockProgressBar, BaseProgressBar


@dataclasses.dataclass
class Video:
    name: str
    url: str


def download_youtube_video(url: str, output_folder: str, filename: str) -> bool:
    try:
        youtube = YouTube(url)
        youtube_video_stream = youtube.streams.get_highest_resolution()

        progress_bar = BlockProgressBar(f"Stahuji {filename}", youtube_video_stream.filesize)
        __setup_listeners(youtube, progress_bar, filename)

        youtube_video_stream.download(output_folder, filename)
        return True
    except VideoUnavailable:
        print(f"\nVideo {url} není dostupné")
    except pytube.exceptions.PytubeError as e:
        print(f"\nNepovdelo se stáhnout video {url}")
    return False


def __setup_listeners(youtube: YouTube, progress_bar: BaseProgressBar, filename: str) -> None:
    def on_progress(stream, _chunk, bytes_remaining) -> None:
        progress_bar.progress(stream.filesize - bytes_remaining)
    youtube.register_on_progress_callback(on_progress)

    def on_complete(_stream, _file_handle) -> None:
        print(f"\n{filename} bylo úspěšně staženo")

    youtube.register_on_complete_callback(on_complete)
