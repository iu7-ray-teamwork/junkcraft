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
            self.__scale = j["scale"]
            self.__mass_center = j["mass_center"]
            self.__sprite_path = j["sprite"]
            self.__density = j["density"]
            self.__contour = j["contour"]
        except KeyError as e:
            raise ValueError(
                error_str.format(path, "Parameter {0} not found".format(e))
            )

        self.__sprite = Image(self.__sprite_path)

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

    @property
    def sprite(self):
        return self.__sprite

    def render(self, surface, transform):
        render(surface, self.__image, transform)
