# coding=UTF-8

import sys
import os
import os.path
import ctypes

if sys.platform.startswith('win32'):
    # assume SDL2.dll is distributed alongside
    os.environ['PYSDL2_DLL_PATH'] = os.path.dirname(__file__)

# stuff inside is prefixed with 'SDL_' anyway
from sdl2 import *

if __name__ == '__main__':
    SDL_Init(SDL_INIT_EVERYTHING)

    window = SDL_CreateWindow(
        b'JunkCraft',
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
        800, 600,
        SDL_WINDOW_RESIZABLE
    )

    event = SDL_Event()
    while event:
        while SDL_PollEvent(ctypes.byref(event)):
            if event.type == SDL_QUIT:
                event = None
                break

    SDL_DestroyWindow(window)

    SDL_Quit()






