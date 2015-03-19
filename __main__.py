#!/usr/bin/env python

from engine import *

if __name__ == "__main__":
    window = Window(title="JunkCraft", size=(800, 600))
    while True:
        for event in get_more_events():
            print(event)
            if type(event) == UserQuitEvent:
                exit()
