from enum import Enum
import cv2

default_pixel_chunk_width = 9
default_pixel_chunk_height = 16


class GreyscaleVariants(Enum):
    GREYSCALE_CHARACTERS_VERBOSE: str = "█$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    GREYSCALE_CHARACTERS_MINIMAL: str = "@#$%?*+;:,."
    GREYSCALE_CHARACTERS_MINIMAL_REVERSED: str = ".,:;+*?%$#@"


class ImageToTextConverter:
    def __init__(
            self,
            pixel_chunk_width: int = default_pixel_chunk_width,
            pixel_chunk_height: int = default_pixel_chunk_height,
            greyscale_characters: str = GreyscaleVariants.GREYSCALE_CHARACTERS_MINIMAL.value
    ):
        self.pixel_chunk_width = pixel_chunk_width
        self.pixel_chunk_height = pixel_chunk_height
        self.greyscale_characters = greyscale_characters
        self.frame = None

    def img_to_text(self, frame) -> str:
        self.frame = frame
        rows, cols, _ = self.frame.shape

        ascii_output = ""
        row_chunks = int(rows / self.pixel_chunk_height)
        col_chunks = int(cols / self.pixel_chunk_width)

        for i in range(row_chunks):
            for j in range(col_chunks):
                row_start = i * self.pixel_chunk_height
                col_start = j * self.pixel_chunk_width
                ascii_output += self.__process_chunk(row_start, col_start)
            ascii_output += "\n"
        return ascii_output

    # TODO zkontronluj, jestli se neskipujou nějaké indexy
    def __process_chunk(self, row_start: int, col_start: int) -> str:
        chunk_brightness = 0
        for row in range(row_start, row_start + self.pixel_chunk_height):
            for col in range(col_start, col_start + self.pixel_chunk_width):
                pixel = self.frame[row, col]
                chunk_brightness += sum(pixel) / len(pixel)

        chunk_brightness /= self.pixel_chunk_width * self.pixel_chunk_height
        ascii_representation_index = int(chunk_brightness / len(self.greyscale_characters)) % len(
            self.greyscale_characters)
        return self.greyscale_characters[ascii_representation_index]
