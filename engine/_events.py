from collections import namedtuple
from ._SDL import *
from ._Window import *


class UserQuitEvent(namedtuple("UserQuitEvent", [])):
    pass


class KeyPressEvent(namedtuple("KeyPressEvent", ["window", "key"])):
    pass


class KeyReleaseEvent(namedtuple("KeyReleaseEvent", ["window", "key"])):
    pass


def get_more_events():
    e = SDL_Event()
    while SDL_PollEvent(e):
        if e.type == SDL_QUIT:
            yield UserQuitEvent()
        elif (e.type in (SDL_KEYDOWN, SDL_KEYUP) and
              e.key.windowID in Window._all):
            event = KeyPressEvent if e.type == SDL_KEYDOWN else KeyReleaseEvent
            yield event(Window._all[e.key.windowID],
                        str(SDL_GetKeyName(e.key.keysym.sym), "UTF-8"))
