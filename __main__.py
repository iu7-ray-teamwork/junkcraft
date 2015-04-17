#!/usr/bin/env python3

from engine import *


if __name__ == "__main__":
    model = Model("resources/rocket.json")

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    scene = Scene()
    scene.objects.add(Object(model))
    scene.objects.add(Object(
        model, math.Matrix.scale(2) * math.Matrix.rotate(math.radians(30)) * math.Matrix.translate(3, 2)))
    scene.objects.add(Object(
        model, math.Matrix.scale(1.5) * math.Matrix.rotate(math.radians(-70)) * math.Matrix.translate(-1, -2)))

    viewport = Viewport(math.Matrix.scale(5))

    def render():
        scene.render(surface, viewport)
        surface.commit()

    render()

    while True:
        for event in get_more_events():
            if event.__class__ == UserQuitEvent:
                exit()
            elif event.__class__ == ResizeEvent:
                if event.window == window:
                    render()
