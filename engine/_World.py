import pymunk

from . import math


class World:
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
        world_to_surface = viewport.world_to(surface)
        for object in self.__objects:
            object.render(surface, world_to_surface)

    def step(self, time_step):
        self.__space.step(time_step)
