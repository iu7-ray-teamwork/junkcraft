import pymunk
import pymunk.constraint


class World:
    def __init__(self, damping=0):
        self._objects = set()
        self._space = pymunk.Space()

        self.damping = damping

    @property
    def objects(self):
        return frozenset(self._objects)

    @property
    def damping(self):
        return 1 - self._space.damping

    @damping.setter
    def damping(self, damping):
        self._space.damping = 1 - damping

    def get_object_at(self, position):
        shape = self._space.point_query_first(tuple(position))
        if shape is None:
            return None
        for object in self._objects:
            if object._body is shape.body:
                return object

    def render(self, surface, viewport):
        world_to_surface = viewport.world_to(surface)
        for object in self._objects:
            object.render(surface, world_to_surface)

    def step(self, time_step):
        for object in self._objects:
            object.step(time_step)
        self._space.step(time_step)
        for object in self._objects:
            object._body.reset_forces()
