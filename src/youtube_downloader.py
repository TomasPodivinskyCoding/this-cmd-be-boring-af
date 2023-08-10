import dataclasses

import pytube.exceptions
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from src.progress_bar import BlockProgressBar


@dataclasses.dataclass
class Video:
    name: str
    url: str


class YoutubeDownloader:
    progress_bar: BlockProgressBar | None = None

    def download_youtube_video(self, url: str, output_folder: str, filename: str) -> None:
        try:
            youtube = YouTube(url, on_progress_callback=self.__on_progress)
        except VideoUnavailable:
            print(f"\nVideo {url} není dostupné")
            return

        youtube = youtube.streams.get_highest_resolution()
        self.progress_bar = BlockProgressBar(f"Stahuji {filename}", youtube.filesize)
        try:
            youtube.download(output_folder, filename)
            print(f"\n{filename} bylo úspěšně staženo")
        except pytube.exceptions.PytubeError:
            print(f"\nNepovdelo se stáhnout video {url}")

    def __on_progress(self, stream, _chunk, bytes_remaining) -> None:
        self.progress_bar.progress(stream.filesize - bytes_remaining)
