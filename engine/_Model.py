import os.path
import json
import pymunk.util

from ._Image import *
from . import math


class Model:
    def __init__(self, path):
        with open(path, "r") as file:
            model = json.load(file)

        self.__images = {}
        if model["image"].__class__ == str:
            model["image"] = {"default": model["image"]}
        for state, image_path in model["image"].items():
            self.__images[state] = Image(os.path.join(os.path.dirname(path), image_path))
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

    def render(self, surface, to_surface, state="default"):
        surface.render_image(self.__images[state], self.__from_image * to_surface)
