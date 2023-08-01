from pytube import YouTube


def download_videos(urls: list[str], output_folder: str) -> None:
    for index, video in enumerate(urls):
        download_youtube_video(video, output_folder, f"video{index + 1}.mp4")


def download_youtube_video(url: str, output_folder: str, filename: str) -> None:
    print(f"Stahuji video {url}")
    youtube = YouTube(url)
    youtube = youtube.streams.get_highest_resolution()
    try:
        downloaded_video = youtube.download(output_folder, filename)
        print(f"Video {downloaded_video} bylo úspěšně staženo")
    except Exception as e:  # TODO mrdat lepší handling errorů
        print(f"Nepovdelo se stáhnout video {url}")


