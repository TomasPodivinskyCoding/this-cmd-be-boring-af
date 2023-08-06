import sys

from pytube import YouTube

from progress_bar import BlockProgressBar

progress_bar: BlockProgressBar | None = None

def download_videos(urls: list[str], output_folder: str) -> None:
    for index, video in enumerate(urls):
        download_youtube_video(video, output_folder, f"video{index + 1}.mp4")


def download_youtube_video(url: str, output_folder: str, filename: str) -> None:
    global progress_bar
    youtube = YouTube(url, on_progress_callback=on_progress)
    youtube = youtube.streams.get_highest_resolution()
    progress_bar = BlockProgressBar(f"Stahuji video {filename}", youtube.filesize)
    try:
        youtube.download(output_folder, filename)
        print(f"\nVideo {filename} bylo úspěšně staženo")
    except Exception as e:  # TODO mrdat lepší handling errorů
        print(f"Nepovdelo se stáhnout video {url}")


def on_progress(stream, chunk, bytes_remaining):
    global progress_bar
    progress_bar.progress(stream.filesize - bytes_remaining)
