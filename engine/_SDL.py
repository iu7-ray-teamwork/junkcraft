import os
import os.path
import sys

if "PYSDL2_DLL_PATH" not in os.environ:
    if sys.platform.startswith("win32"):
        # assume SDL2.dll is distributed alongside
        os.environ["PYSDL2_DLL_PATH"] = os.path.join(
            os.path.dirname(__file__), "binaries")

from sdl2 import *  # noqa

SDL_Init(SDL_INIT_EVERYTHING)
