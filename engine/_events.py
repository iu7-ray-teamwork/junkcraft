__all__ = []

from collections import namedtuple

from ._sdl import *
from ._Window import *

__all__ += ["UserQuitEvent"]
class UserQuitEvent(namedtuple("UserQuitEvent", [])):
    pass

__all__ += ["KeyPressEvent"]
class KeyPressEvent(namedtuple("KeyPressEvent", ["window", "key"])):
    pass

__all__ += ["KeyReleaseEvent"]
class KeyReleaseEvent(namedtuple("KeyReleaseEvent", ["window", "key"])):
    pass

__all__ += ["get_more_events"]
def get_more_events():
    e = SDL_Event()
    while SDL_PollEvent(e):
        if e.type == SDL_QUIT:
            yield UserQuitEvent()
        elif e.type == SDL_KEYDOWN:
            if e.key.windowID in Window._all:
                yield KeyPressEvent(Window._all[e.key.windowID], str(SDL_GetKeyName(e.key.keysym.sym), 'UTF-8'))
        elif e.type == SDL_KEYUP:
            if e.key.windowID in Window._all:
                yield KeyReleaseEvent(Window._all[e.key.windowID], str(SDL_GetKeyName(e.key.keysym.sym), 'UTF-8'))
