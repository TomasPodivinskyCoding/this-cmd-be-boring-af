import time
from enum import Enum

import cv2
import numpy
import numpy as np


class GreyscaleVariants(Enum):
    DEPTH_70: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    DEPTH_70_REVERSED: str = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    DEPTH_10: str = "@#$%?*+;:,."
    DEPTH_10_REVERSED: str = ".,:;+*?%$#@"


class ImageToTextConverter:
    grayscale_length: int
    new_width: int

    def __init__(
            self,
            dimensions: tuple[int, int],
            new_width: int = 100,
            greyscale_characters: GreyscaleVariants = GreyscaleVariants.DEPTH_10_REVERSED
    ):
        self.new_width = new_width
        self.new_height = self.__calculate_new_height(dimensions)
        self.greyscale_characters = greyscale_characters.value
        self.rgb_weights = np.array([0.1140, 0.5870, 0.2989])

    def __calculate_new_height(self, dimensions: tuple[int, int]) -> int:
        ascii_character_aspect_ratio = 0.55
        aspect_ratio = dimensions[1] / float(dimensions[0])
        return int(self.new_width / aspect_ratio * ascii_character_aspect_ratio)

    def img_to_text(self, img: np.ndarray) -> str:
        if img is None:
            return ""

        img_resized = cv2.resize(img, (self.new_width, self.new_height))
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        img_normalized = (img_gray / 255.0) * (len(self.greyscale_characters) - 1)

        ascii_img = np.asarray([self.greyscale_characters[int(pix)] for pix in np.nditer(img_normalized)])
        ascii_img = ascii_img.reshape((self.new_height, self.new_width))
        return "\n".join(["".join(row) for row in ascii_img])
