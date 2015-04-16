from collections import namedtuple
from ._SDL import *
from ._Window import *


class UserQuitEvent(namedtuple("UserQuitEvent", [])):
    pass


class ResizeEvent(namedtuple("ResizeEvent", ["window", "new_size"])):
    pass


class KeyPressEvent(namedtuple("KeyPressEvent", ["window", "key"])):
    pass


class KeyReleaseEvent(namedtuple("KeyReleaseEvent", ["window", "key"])):
    pass

_key_events = {
    SDL_KEYDOWN: KeyPressEvent,
    SDL_KEYUP: KeyReleaseEvent,
}

def get_more_events():
    e = SDL_Event()
    while SDL_PollEvent(e):
        if e.type == SDL_QUIT:
            yield UserQuitEvent()
        elif e.type == SDL_WINDOWEVENT and e.window.windowID in Window._all:
            window = Window._all[e.window.windowID]
            if e.window.event == SDL_WINDOWEVENT_SIZE_CHANGED:
                new_size = e.window.data1, e.window.data2
                yield ResizeEvent(window, new_size)
        elif e.type in _key_events and e.key.windowID in Window._all:
            event = _key_events[e.type]
            window = Window._all[e.key.windowID]
            key = str(SDL_GetKeyName(e.key.keysym.sym), "UTF-8")
            yield event(window, key)
