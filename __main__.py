#!/usr/bin/env python

from engine import *

if __name__ == "__main__":
    window = Window(title="JunkCraft", size=(800, 600))
    surface = Surface(window)
    image = Image("resources/leaf.png")
    render(surface, image, math.Matrix.rotate(math.radians(45)) * math.Matrix.translate(0.5, 0))
    surface.commit()

    while True:
        for event in get_more_events():
            print(event)
            if type(event) == UserQuitEvent:
                exit()
