import engine


class Thruster(engine.Object):
    def __init__(self, world, *, force, **kwargs):
        super().__init__(world, engine.Model("resources/thruster.json"), **kwargs)
        self.force = force

    def render(self, surface, world_to_surface):
        self.model.render(surface, self.to_world * world_to_surface, "active" if self.active else "default")

    def step(self, time_step):
        to_world = self.to_world
        direction = engine.math.Vector.unit_y * to_world - engine.math.Vector.zero * to_world
        if self.active:
            self.apply_force(direction * self.force)
