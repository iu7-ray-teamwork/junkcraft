#!/usr/bin/env python3

import random

from engine import *


if __name__ == "__main__":
    model = Model("resources/rocket.json")

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    world = World(damping=0.3)

    player = Object(
        world,
        model,
        scale=0.5
    )

    viewport = Viewport(player, scale=10)

    for i in range(random.randint(10, 20)):
        Object(
            world,
            model,
            position=(random.uniform(-5, 5), random.uniform(-5, 5)),
            angle=random.uniform(0, 2 * math.pi),
            scale=random.uniform(0.5, 2)
        )

    pressed_keys = set()

    player_pin_point = None
    unpin_target = None

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
                    player_pin_point = position
                    if world.object_at(player_pin_point) is not player:
                        player_pin_point = None
                elif event.button == "Right":
                    unpin_target = world.object_at(position)
            elif event.__class__ == MouseButtonReleaseEvent:
                if event.button == "Left":
                    if player_pin_point is not None:
                        junk_pin_point = event.position * ~viewport.world_to(surface)
                        junk = world.object_at(junk_pin_point)
                        if junk is not None:
                            player.pin(junk, player_pin_point, junk_pin_point)
                        player_pin_point = None
                elif event.button == "Right":
                    if unpin_target is not None:
                        print(unpin_target)
                        unpin_target.unpin()

        force = 10

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
