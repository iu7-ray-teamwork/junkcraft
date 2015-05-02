#!/usr/bin/env python3

import random

from engine import *
from _Player import *


if __name__ == "__main__":
    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    world = World(damping=0.3)

    player = Player(world)

    viewport = Viewport(player, scale=10)

    rocket_model = Model("resources/rocket.json")
    for i in range(random.randint(10, 20)):
        Object(
            world,
            rocket_model,
            position=(random.uniform(-5, 5), random.uniform(-5, 5)),
            angle=random.uniform(0, 2 * math.pi),
            scale=random.uniform(0.5, 2)
        )

    pressed_keys = set()

    for time_step in time_steps(1 / 60):
        for event in get_more_events():
            if event.__class__ == UserQuitEvent:
                exit()
            elif event.__class__ == KeyPressEvent:
                pressed_keys.add(event.key)
            elif event.__class__ == KeyReleaseEvent:
                pressed_keys.discard(event.key)
            elif event.__class__ == MouseButtonPressEvent:
                position = event.position * ~viewport.world_to(surface)
                if event.button == "Left":
                    attach_a_point = position
                    attach_a = world.get_object_at(attach_a_point)
                    if attach_a is not None:
                        attach_a_point *= ~attach_a.to_world
                elif event.button == "Right":
                    detach_a = world.get_object_at(position)
            elif event.__class__ == MouseButtonReleaseEvent:
                position = event.position * ~viewport.world_to(surface)
                if event.button == "Left":
                    if attach_a is not None:
                        attach_a_point *= attach_a.to_world
                        attach_b_point = position
                        attach_b = world.get_object_at(attach_b_point)
                        if attach_b is not None:
                            player.attach(attach_a, attach_b, attach_a_point, attach_b_point)
                elif event.button == "Right":
                    if detach_a is not None:
                        detach_b = world.get_object_at(position)
                        if detach_b is not None:
                            player.detach(detach_a, detach_b)

        force = 100

        ptw = player.to_world

        o = math.Vector.zero * ptw

        if "W" in pressed_keys:
            player.apply_force(math.Vector(0, +force) * ptw - o)
        if "A" in pressed_keys:
            player.apply_force(math.Vector(-force, 0) * ptw - o)
        if "S" in pressed_keys:
            player.apply_force(math.Vector(0, -force) * ptw - o)
        if "D" in pressed_keys:
            player.apply_force(math.Vector(+force, 0) * ptw - o)

        world.step(time_step)

        surface.clear()
        world.render(surface, viewport)
        surface.commit()
