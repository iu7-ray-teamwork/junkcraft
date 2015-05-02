import pymunk

from . import math


class Scene:
    def __init__(self, damping=0):
        self.__objects = set()
        self.__space = pymunk.Space()
        self.damping = damping

    @property
    def damping(self):
        return 1 - self.__space.damping

    @damping.setter
    def damping(self, damping):
        self.__space.damping = 1 - damping

    def add(self, object):
        self.__objects.add(object)
        self.__space.add(object._body, *object._shapes)

    def render(self, surface, viewport):
        size = surface.size
        viewport_to_surface = math.Matrix.scale(max(size) * math.Vector(+0.5, -0.5)) * math.Matrix.translate(size / 2)
        scene_to_surface = ~viewport.to_scene * viewport_to_surface
        for object in self.__objects:
            object.render(surface, scene_to_surface)

    def step(self, time_step):
        self.__space.step(time_step)
