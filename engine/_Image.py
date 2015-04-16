from PIL.Image import open as PIL_Image_open

from . import math


class Image:
    def __init__(self, path):
        image = PIL_Image_open(path).convert("RGBA")
        self.__size = math.Vector(image.size)
        self.__data = image.tobytes("raw")

    @property
    def size(self):
        return self.__size

    @property
    def data(self):
        return self.__data
