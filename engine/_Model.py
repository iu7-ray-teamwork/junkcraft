import os.path
import json
import pymunk.util

from ._Image import *
from . import math


class Model:
    def __init__(self, path):
        with open(path, "r") as file:
            model = json.load(file)

        self.__image = Image(os.path.join(os.path.dirname(path), model["image"]))
        self.__density = model.get("density", 1.0)
        self.__elasticity = model.get("elasticity", 0.0)
        self.__friction = model.get("friction", 0.0)

        shape = model["shape"]
        xs, ys = zip(*shape)
        lx, ly = min(xs), min(ys)
        hx, hy = max(xs), max(ys)
        if "mass_center" not in model:
            model["mass_center"] = pymunk.util.calc_center(shape)
        mass_center = math.Vector(model["mass_center"])
        scale = model["size"] / max(hx - lx, hy - ly)
        self.__from_image = math.Matrix.translate(-mass_center) * math.Matrix.scale(+scale, -scale)

        self.__shape = tuple(map(lambda x, y: math.Vector(x, y) * self.__from_image, xs, ys))

    @property
    def image(self):
        return self.__image

    @property
    def density(self):
        return self.__density

    @property
    def elasticity(self):
        return self.__elasticity

    @property
    def friction(self):
        return self.__friction

    @property
    def shape(self):
        return self.__shape

    def render(self, surface, to_surface):
        surface.render_image(self.__image, self.__from_image * to_surface)
