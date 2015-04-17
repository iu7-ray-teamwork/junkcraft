import os.path
import json

from ._Image import *
from ._render import *


class Model:
    def __init__(self, path):
        error_str = "Corrupted json file '{0}'. Reason: {1}"

        with open(path, "r") as file:
            try:
                j = json.load(file)
            except ValueError as e:
                raise ValueError(error_str.format(path, str(e)))

        try:
            image_path = j["image"]
            self.__scale = j["scale"]
            self.__mass_center = j["mass_center"]
            self.__density = j["density"]
            self.__contour = j["contour"]
        except KeyError as e:
            raise ValueError(error_str.format(path, "Parameter {0} not found".format(e)))

        self.__image = Image(os.path.join(os.path.dirname(path), image_path))

    @property
    def image(self):
        return self.__image

    @property
    def scale(self):
        return self.__scale

    @property
    def mass_center(self):
        return self.__mass_center

    @property
    def density(self):
        return self.__density

    @property
    def contour(self):
        return self.__contour

    def render(self, surface, transform):
        render(surface, self.__image, transform)
