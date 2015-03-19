__all__ = []

import os
import os.path
import sys

if "PYSDL2_DLL_PATH" not in os.environ:
    if sys.platform.startswith('win32'):
        # assume SDL2.dll is distributed alongside
        os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.path.dirname(__file__), "binaries")

from sdl2 import *
import sdl2
__all__ += (n for n in dir(sdl2) if not n.startswith("_"))

SDL_Init(SDL_INIT_EVERYTHING)
