from . import math


class Object:
    def __init__(self, model, to_scene=math.Matrix.identity):
        self.__model = model
        self.to_scene = to_scene

    @property
    def model(self):
        return self.__model

    def render(self, surface, scene_to_surface):
        self.__model.render(surface, self.to_scene * scene_to_surface)
