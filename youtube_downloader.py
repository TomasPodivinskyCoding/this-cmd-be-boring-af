import sys

from pytube import YouTube

from progress_bar import BlockProgressBar


class YoutubeDownloader:
    progress_bar: BlockProgressBar | None = None

    def download_videos(self, urls: list[str], output_folder: str) -> None:
        for index, video in enumerate(urls):
            self.download_youtube_video(video, output_folder, f"video{index + 1}.mp4")


    def download_youtube_video(self, url: str, output_folder: str, filename: str) -> None:
        youtube = YouTube(url, on_progress_callback=self.on_progress)
        youtube = youtube.streams.get_highest_resolution()
        self.progress_bar = BlockProgressBar(f"Stahuji {filename}", youtube.filesize)
        try:
            youtube.download(output_folder, filename)
            print(f"\n{filename} bylo úspěšně staženo")
        except Exception as e:  # TODO mrdat lepší handling errorů
            print(f"\nNepovdelo se stáhnout video {url}")


    def on_progress(self, stream, chunk, bytes_remaining) -> None:
        self.progress_bar.progress(stream.filesize - bytes_remaining)
