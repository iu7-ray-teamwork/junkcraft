from . import math


class Viewport:
    def __init__(self, object, scale=1):
        self.object = object
        self.scale = scale

    def world_to(self, surface):
        size = surface.size
        to_surface = math.Matrix.scale(max(size) * math.Vector(+0.5, -0.5)) * math.Matrix.translate(size / 2)
        to_world = math.Matrix.scale(self.scale) * self.object.to_world
        return ~to_world * to_surface