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
        contour = model["contour"]
        lx, ly = None, None
        hx, hy = None, None
        for x, y in contour:
            if lx is None or x < lx:
                lx = x
            elif hx is None or x > hx:
                hx = x
            if ly is None or y < ly:
                ly = y
            elif hy is None or y > hy:
                hy = y
        contour_center = math.Vector(hx + lx, hy + ly) / 2
        scale = self.__size / max(hx - lx, hy - ly)
        self.__from_image = math.Matrix.translate(-contour_center) * math.Matrix.scale(+scale, -scale)
        self.__contour = tuple(map(lambda cp: math.Vector(cp) * self.__from_image, contour))

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
