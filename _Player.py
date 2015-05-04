import collections

import engine

from _Thruster import *


class Player(engine.Object):
    def __init__(self, world, **kwargs):
        super().__init__(world, engine.Model("resources/fridge.json"), **kwargs)

        self.__pressed_keys = set()
        self.__wiring = collections.defaultdict(set)

        thruster = Thruster(world,
                            position=engine.math.Vector(+0.35, -0.5) * self.to_world,
                            force=40)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world * self.to_world,
                    min(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world,
                    max(filter(lambda p: p.x > 0, thruster.model.shape), key=lambda p: p.y) * thruster.to_world)
        self.attach(self, thruster,
                    min(filter(lambda p: p.x < 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    min(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    min(filter(lambda p: p.x < 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.y) * thruster.to_world)
        self.wire(thruster, "W")
        self.wire(thruster, "A")

        thruster = Thruster(world,
                            position=engine.math.Vector(-0.35, -0.5) * self.to_world,
                            force=40)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world,
                    max(filter(lambda p: p.x > 0, thruster.model.shape), key=lambda p: p.y) * thruster.to_world)
        self.attach(self, thruster,
                    min(filter(lambda p: p.x > 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    min(filter(lambda p: p.x > 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.y) * thruster.to_world)
        self.wire(thruster, "W")
        self.wire(thruster, "D")

    def attach(self, a, b, a_point, b_point):
        pinned_objects = self.compute_pinned_objects()
        if a in pinned_objects or b in pinned_objects:
            a.pin(b, a_point, b_point)

    def detach(self, a, b):
        pinned_objects = self.compute_pinned_objects()
        if a in pinned_objects or b in pinned_objects:
            a.unpin(b)

    def on_key_press(self, key):
        self.__pressed_keys.add(key)

    def on_key_release(self, key):
        self.__pressed_keys.discard(key)

    def wire(self, target, activation_key):
        if target in self.compute_pinned_objects():
            self.__wiring[target].add(activation_key)

    def step(self, time_step):
        for object, activation_keys in self.__wiring.items():
            object.active = bool(activation_keys & self.__pressed_keys)
