#!/usr/bin/env python3

import random

from engine import *


if __name__ == "__main__":
    model = Model("resources/rocket.json")

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    viewport = Viewport(math.Matrix.scale(5))

    scene = Scene()

    player = Object(model)
    scene.add(player)

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

        if "W" in pressed_keys:
            player.apply_force((0, force))
        if "A" in pressed_keys:
            player.apply_force((-force, 0))
        if "S" in pressed_keys:
            player.apply_force((0, -force))
        if "D" in pressed_keys:
            player.apply_force((force, 0))

        scene.step(time_step)

        player.reset_forces()

        surface.clear()
        scene.render(surface, viewport)
        surface.commit()
