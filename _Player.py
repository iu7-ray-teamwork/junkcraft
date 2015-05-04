import collections

import engine

from _Thruster import *


class Player(engine.Object):
    def __init__(self, world, *, thruster_force, **kwargs):
        super().__init__(world, engine.Model("resources/fridge.json"), **kwargs)

        self.__pressed_keys = set()
        self.__wiring = collections.defaultdict(set)

        thruster = Thruster(world,
                            position=engine.math.Vector(+0.35, -0.5) * self.to_world,
                            force=thruster_force)
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
                            force=thruster_force)
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

        thruster = Thruster(world,
                            position=engine.math.Vector(+0.35, +0.5) * self.to_world,
                            angle=engine.math.pi,
                            force=thruster_force)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world,
                    max(filter(lambda p: p.x > 0, thruster.model.shape), key=lambda p: p.y) * thruster.to_world)
        self.attach(self, thruster,
                    max(filter(lambda p: p.x > 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    max(filter(lambda p: p.x > 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.y) * thruster.to_world)
        self.wire(thruster, "S")
        self.wire(thruster, "D")

        thruster = Thruster(world,
                            position=engine.math.Vector(-0.35, +0.5) * self.to_world,
                            angle=engine.math.pi,
                            force=thruster_force)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world * self.to_world,
                    min(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    engine.math.Vector.zero * self.to_world,
                    max(filter(lambda p: p.x > 0, thruster.model.shape), key=lambda p: p.y) * thruster.to_world)
        self.attach(self, thruster,
                    max(filter(lambda p: p.x < 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    min(thruster.model.shape, key=lambda p: p.x) * thruster.to_world)
        self.attach(self, thruster,
                    max(filter(lambda p: p.x < 0, self.model.shape), key=lambda p: p.y) * self.to_world,
                    max(thruster.model.shape, key=lambda p: p.y) * thruster.to_world)
        self.wire(thruster, "S")
        self.wire(thruster, "A")

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

    def unwire(self, target, activation_key):
        if target is None:
            if activation_key is None:
                self.__wiring.clear()
            else:
                for target, activation_keys in self.__wiring:
                    activation_keys.discard(activation_key)
        elif target in self.compute_pinned_objects():
            if activation_key is None:
                self.__wiring[target].clear()
            else:
                self.__wiring[target].discard(activation_key)

    def on_after_input(self):
        pinned_objects = self.compute_pinned_objects()
        for target, activation_keys in self.__wiring.items():
            if target in pinned_objects:
                target.active = bool(activation_keys & self.__pressed_keys)
