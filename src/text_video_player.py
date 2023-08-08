import time

import colorama


class TextVideoPlayer:
    text_frames: list[str]
    delay: float

    def __init__(self, text_frames: list[str], fps: int = 60):
        self.text_frames = text_frames
        self.delay = 1 / fps

        colorama.init()

    def play(self):
        new_lines_number = self.text_frames[0].count("\n")
        go_up_a_row_char = '\033[A'
        go_to_start_of_previous_output = go_up_a_row_char * new_lines_number

        for text_frame in self.text_frames:
            print(text_frame + go_to_start_of_previous_output, end="\r")
            time.sleep(self.delay)
        print("\n" * new_lines_number)
