from . import math


class Viewport:
    def __init__(self, object, *, min_scale, max_scale, scale=None):
        self.object = object
        self.__min_scale = min_scale
        self.__max_scale = max_scale
        self.__scale = math.sqrt(min_scale * max_scale)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = math.clamp(self.__min_scale, scale, self.__max_scale)

    def world_to(self, surface):
        size = surface.size
        to_surface = math.Matrix.scale(max(size) * math.Vector(+0.5, -0.5)) * math.Matrix.translate(size / 2)
        to_world = math.Matrix.scale(self.scale) * self.object.to_world
        return ~to_world * to_surface
