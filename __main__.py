#!/usr/bin/env python3

from engine import *


if __name__ == "__main__":
    image = Image("resources/leaf.png")

    def draw_scene(surface):
        render(surface, image,
               math.Matrix.rotate(math.radians(45)) *
               math.Matrix.translate(0.5, 0))
        surface.commit()

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    draw_scene(surface)

    while True:
        for event in get_more_events():
            if event.__class__ == UserQuitEvent:
                exit()
            elif event.__class__ == ResizeEvent:
                if event.window == window:
                    draw_scene(surface)
