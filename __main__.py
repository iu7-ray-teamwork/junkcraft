#!/usr/bin/env python3

import random

import engine

from _Player import *
from _Thruster import *

if __name__ == "__main__":
    window = engine.Window(title="JunkCraft", size=(800, 600))
    surface = engine.Surface(window)

    world = engine.World(damping=0.3)

    player = Player(world,
                    thruster_force=40)

    viewport = engine.Viewport(player, scale=10)

    asteroid_models = []
    for i in range(4):
        asteroid_models.append(engine.Model("resources/asteroid{}.json".format(i)))
    for i in range(random.randint(20, 50)):
        engine.Object(world, random.choice(asteroid_models),
                      position=(random.uniform(-20, 20), random.uniform(-20, 20)),
                      angle=random.uniform(0, 2 * engine.math.pi),
                      scale=random.uniform(0.1, 2))

    for i in range(random.randint(10, 20)):
        scale = random.uniform(1, 3)
        Thruster(world,
                 position=(random.uniform(-20, 20), random.uniform(-20, 20)),
                 angle=random.uniform(0, 2 * engine.math.pi),
                 scale=scale,
                 force=40 * scale)

    attach_a_point = None
    attach_a = None
    attach_b_point = None
    attach_b = None
    wire_target = None
    unwiring = False

    for time_step in engine.time_steps(1 / 60):
        for event in engine.get_more_events():
            if event.__class__ == engine.UserQuitEvent:
                exit()
            elif event.__class__ == engine.KeyPressEvent:
                if wire_target is not None:
                    if event.key == "Delete":
                        if unwiring:
                            player.unwire(None if wire_target is player else wire_target, None)
                        else:
                            unwiring = True
                    else:
                        if unwiring:
                            player.unwire(None if wire_target is player else wire_target, event.key)
                        elif wire_target is not player:
                            player.wire(wire_target, event.key)
                else:
                    player.on_key_press(event.key)
            elif event.__class__ == engine.KeyReleaseEvent:
                player.on_key_release(event.key)
            elif event.__class__ == engine.MouseButtonPressEvent:
                position = event.position * ~viewport.world_to(surface)
                if event.button == "Left":
                    attach_a_point = position
                    attach_a = world.get_object_at(attach_a_point)
                    if attach_a is not None:
                        attach_a_point *= ~attach_a.to_world
                elif event.button == "Right":
                    detach_a = world.get_object_at(position)
                elif event.button == "Wheel":
                    wire_target = world.get_object_at(position)
            elif event.__class__ == engine.MouseButtonReleaseEvent:
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
                elif event.button == "Wheel":
                    wire_target = None
                    unwiring = False

        world.after_input()

        world.before_physics()
        world.physics(time_step)
        world.after_physics()

        surface.clear()
        world.render(surface, viewport)
        surface.commit()
