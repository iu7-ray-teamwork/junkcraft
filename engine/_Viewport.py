from . import math


class Viewport:
    def __init__(self, object, scale=1):
        self.object = object
        self.scale = scale

    @property
    def to_world(self):
        return math.Matrix.scale(self.scale) * self.object.to_world
