from . import math


class Viewport:
    def __init__(self, to_scene=math.Matrix.identity):
        self.to_scene = to_scene
