import weakref

import pymunk
import pymunk.util
import pymunk.constraint

from . import math


class Object:
    def __init__(self, world, model, *, position=(0, 0), angle=0, scale=1):
        self.__world = weakref.ref(world)
        self.__model = model

        self.__scale = math.Matrix.scale(scale)

        shape = model.shape
        if pymunk.util.is_clockwise(shape):
            shape = reversed(shape)
        shape = list(map(lambda p: p * self.__scale, shape))

        mass = model.density * pymunk.util.calc_area(shape)
        self._body = pymunk.Body(mass, pymunk.moment_for_poly(mass, shape))
        self._body.__object = weakref.ref(self)
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

        self.active = False

    @property
    def world(self):
        return self.__world()

    @property
    def model(self):
        return self.__model

    @property
    def to_world(self):
        return self.__scale * math.Matrix.rotate(self._body.angle) * math.Matrix.translate(self._body.position)

    def apply_force(self, force, point=None):
        if point is None:
            self._body.apply_force(tuple(force))
        else:
            self._body.apply_force(tuple(force), tuple(point - math.Vector.zero * self.to_world))

    def reset_forces(self):
        self._body.reset_forces()

    def pin(self, other, self_point, other_point):
        self_point = tuple(math.Vector(self_point) * ~self.to_world)
        other_point = tuple(math.Vector(other_point) * ~other.to_world)
        self.world._space.add(pymunk.constraint.PinJoint(self._body, other._body, self_point, other_point))

    def unpin(self, other):
        for constraint in self._body.constraints:
            if constraint.__class__ == pymunk.constraint.PinJoint:
                if constraint.a is other._body or constraint.b is other._body:
                    self.world._space.remove(constraint)

    def compute_pinned_objects(self):
        objects = set()

        new_objects = {self}
        while new_objects:
            objects |= new_objects
            new_objects.clear()
            for object in objects:
                for constraint in object._body.constraints:
                    for body in (constraint.a, constraint.b):
                        body_object = body.__object()
                        if body_object not in objects and body_object not in new_objects:
                            new_objects.add(body_object)

        return objects

    def render(self, surface, world_to_surface):
        self.__model.render(surface, self.to_world * world_to_surface)

    def on_after_input(self):
        pass

    def on_before_physics(self):
        pass

    def on_after_physics(self):
        pass
