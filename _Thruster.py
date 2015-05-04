import engine


class Thruster(engine.Object):
    def __init__(self, world, *, force, **kwargs):
        super().__init__(world, engine.Model("resources/thruster.json"), **kwargs)
        self.force = force

    def render(self, surface, world_to_surface):
        self.model.render(surface, self.to_world * world_to_surface, "active" if self.active else "default")

    def on_before_physics(self):
        to_world = self.to_world
        if self.active:
            self.apply_force(engine.math.Vector(0, self.force) * to_world - engine.math.Vector.zero * to_world)

    def on_after_physics(self):
        self.reset_forces()
