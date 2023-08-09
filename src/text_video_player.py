import time

import colorama


class TextVideoPlayer:
    text_frames: list[str]
    delay: float
    go_to_start_of_previous_output: str
    new_lines_number: int

    def __init__(self, text_frames: list[str], fps: int = 60):
        self.text_frames = text_frames
        self.delay = 1 / fps

        go_up_a_row_char = '\033[A'
        self.new_lines_number = self.text_frames[0].count("\n")
        self.go_to_start_of_previous_output = go_up_a_row_char * self.new_lines_number

        colorama.init()

    def play(self):
        for text_frame in self.text_frames:
            print(text_frame + self.go_to_start_of_previous_output, end="\r")
            time.sleep(self.delay)
        print("\n" * self.new_lines_number)
