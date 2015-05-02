#!/usr/bin/env python3

import random

from engine import *


if __name__ == "__main__":
    model = Model("resources/rocket.json")

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    scene = Scene(damping=0.3)

    player = Object(
        model,
        scale=0.5)
    scene.add(player)

    viewport = Viewport(player, scale=10)

    for i in range(random.randint(10, 20)):
        scene.add(Object(
            model,
            position=(random.uniform(-5, 5), random.uniform(-5, 5)),
            angle=random.uniform(0, 2 * math.pi),
            scale=random.uniform(0.5, 2)))

    pressed_keys = set()

    for time_step in time_steps(1 / 60):
        for event in get_more_events():
            if event.__class__ == UserQuitEvent:
                exit()
            elif event.__class__ == KeyPressEvent:
                pressed_keys.add(event.key)
            elif event.__class__ == KeyReleaseEvent:
                pressed_keys.discard(event.key)

        force = 10

        pts = player.to_scene

        o = math.Vector.zero * pts

        if "W" in pressed_keys:
            player.apply_force(math.Vector(0, +force) * pts - o)
        if "A" in pressed_keys:
            player.apply_force(math.Vector(-force, 0) * pts - o)
        if "S" in pressed_keys:
            player.apply_force(math.Vector(0, -force) * pts - o)
        if "D" in pressed_keys:
            player.apply_force(math.Vector(+force, 0) * pts - o)

        scene.step(time_step)

        player.reset_forces()

        surface.clear()
        scene.render(surface, viewport)
        surface.commit()
