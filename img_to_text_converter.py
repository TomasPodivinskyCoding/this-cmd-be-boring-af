import time
from enum import Enum

import numpy
import numpy as np

default_pixel_chunk_width = 9
default_pixel_chunk_height = 16


class GreyscaleVariants(Enum):
    GREYSCALE_CHARACTERS_VERBOSE: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    GREYSCALE_CHARACTERS_MINIMAL: str = "@#$%?*+;:,."
    GREYSCALE_CHARACTERS_MINIMAL_REVERSED: str = ".,:;+*?%$#@"


class ImageToTextConverter:
    frame: numpy.ndarray | None
    grayscale_length: int
    brightness_factor: float

    def __init__(
            self,
            pixel_chunk_width: int = default_pixel_chunk_width,
            pixel_chunk_height: int = default_pixel_chunk_height,
            greyscale_characters: str = GreyscaleVariants.GREYSCALE_CHARACTERS_MINIMAL_REVERSED.value
    ):
        self.pixel_chunk_width = pixel_chunk_width
        self.pixel_chunk_height = pixel_chunk_height
        self.greyscale_characters = greyscale_characters
        self.brightness_factor = (len(self.greyscale_characters) - 1) / 255
        self.frame = None

    def img_to_text(self, frame: numpy.ndarray) -> str:
        self.frame = frame
        rows, cols = self.frame.shape

        row_chunks = rows // self.pixel_chunk_height
        col_chunks = cols // self.pixel_chunk_width

        ascii_output = [
            ''.join(
                self.__process_chunk(i * self.pixel_chunk_height, j * self.pixel_chunk_width)
                for j in range(col_chunks)
            )
            for i in range(row_chunks)
        ]

        return '\n'.join(ascii_output)

    def __process_chunk(self, row_start: int, col_start: int) -> str:
        frame_slice = self.frame[
                      row_start:row_start + self.pixel_chunk_height,
                      col_start:col_start + self.pixel_chunk_width
                      ]

        chunk_brightness = np.mean(frame_slice)
        ascii_representation_index = int(chunk_brightness * self.brightness_factor)

        return self.greyscale_characters[ascii_representation_index]