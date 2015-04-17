#!/usr/bin/env python3

from engine import *


if __name__ == "__main__":
    model = Model("resources/rocket.json")

    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)

    def draw_scene():
        model.render(surface, math.Matrix.translate(window.size / 2))
        # surface.render_image(image,
        #                      math.Matrix.translate((window.size - image.size) / 2) *
        #                      math.Matrix.rotate(math.radians(30), origin=window.size / 2))
        surface.commit()

    draw_scene()

    while True:
        for event in get_more_events():
            if event.__class__ == UserQuitEvent:
                exit()
            elif event.__class__ == ResizeEvent:
                if event.window == window:
                    draw_scene()
