import os.path
import json

from ._Image import *
from . import math


class Model:
    def __init__(self, path):
        with open(path, "r") as file:
            model = json.load(file)

        self.__image = Image(os.path.join(os.path.dirname(path), model["image"]))
        self.__size = model["size"]
        self.__density = model["density"]
        xs, ys = zip(*model["contour"])
        lx, ly = min(xs), min(ys)
        hx, hy = max(xs), max(ys)
        center = math.Vector(hx + lx, hy + ly) / 2
        scale = self.__size / max(hx - lx, hy - ly)
        self.__from_image = math.Matrix.translate(-center) * math.Matrix.scale(+scale, -scale)
        self.__contour = tuple(map(lambda x, y: math.Vector(x, y) * self.__from_image, xs, ys))

    @property
    def image(self):
        return self.__image

    @property
    def size(self):
        return self.__size

    @property
    def density(self):
        return self.__density

    @property
    def contour(self):
        return self.__contour

    def render(self, surface, to_surface):
        surface.render_image(self.__image, self.__from_image * to_surface)
