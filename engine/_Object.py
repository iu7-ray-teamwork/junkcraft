import pymunk
import pymunk.util

from . import math


class Object:
    def __init__(self, model, position=(0, 0), angle=0, scale=1):
        self.__model = model
        self.__scale = math.Matrix.scale(scale)

        shape = model.shape
        if pymunk.util.is_clockwise(shape):
            shape = reversed(shape)
        shape = list(map(lambda p: p * self.__scale, shape))

        mass = model.density * pymunk.util.calc_area(shape)
        self._body = pymunk.Body(mass, pymunk.moment_for_poly(mass, shape))
        self._body.position = tuple(position)
        self._body.angle = angle
        self._shapes = []
        for convex_polygon in pymunk.util.convexise(pymunk.util.triangulate(shape)):
            convex_polygon = pymunk.Poly(self._body, convex_polygon)
            convex_polygon.elasticity = model.elasticity
            convex_polygon.friction = model.friction
            self._shapes.append(convex_polygon)

    @property
    def to_scene(self):
        return self.__scale * math.Matrix.rotate(self._body.angle) * math.Matrix.translate(self._body.position)

    def apply_force(self, force, point=None):
        if point is None:
            self._body.apply_force(tuple(force))
        else:
            self._body.apply_force(tuple(force), tuple(point - math.Vector.zero * self.to_scene))

    def reset_forces(self):
        self._body.reset_forces()

    def render(self, surface, scene_to_surface):
        self.__model.render(surface, self.to_scene * scene_to_surface)
