import weakref

import pymunk
import pymunk.util
import pymunk.constraint

from . import math


class Object:
    def __init__(self, world, model, position=(0, 0), angle=0, scale=1):
        self.__world = weakref.ref(world)
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

        world._objects.add(self)
        world._space.add(self._body, *self._shapes)

    @property
    def world(self):
        return self.__world()

    @property
    def to_world(self):
        return self.__scale * math.Matrix.rotate(self._body.angle) * math.Matrix.translate(self._body.position)

    def apply_force(self, force, point=None):
        if point is None:
            self._body.apply_force(tuple(force))
        else:
            self._body.apply_force(tuple(force), tuple(point - math.Vector.zero * self.to_world))

    def pin(self, other, self_point=None, other_point=None):
        self_point = (0, 0) if self_point is None else tuple(math.Vector(self_point) * ~self.to_world)
        other_point = (0, 0) if other_point is None else tuple(math.Vector(other_point) * ~other.to_world)
        self.world._space.add(pymunk.constraint.PinJoint(self._body, other._body, self_point, other_point))

    def unpin(self):
        for constraint in self._body.constraints:
            if constraint.__class__ == pymunk.constraint.PinJoint:
                self.world._space.remove(constraint)

    def render(self, surface, world_to_surface):
        self.__model.render(surface, self.to_world * world_to_surface)
