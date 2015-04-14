from PIL.Image import open as open_image


class Image:
    def __init__(self, path):
        image = open_image(path).convert("RGBA")
        self.__size = image.size
        self.__data = image.tobytes("raw")

    @property
    def size(self):
        return self.__size

    @property
    def data(self):
        return self.__data
