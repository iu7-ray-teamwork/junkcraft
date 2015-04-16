import collections
import weakref

from ._SDL import *
from ._GL import *
from ._Window import *

UserQuitEvent = collections.namedtuple("UserQuitEvent", [])
ResizeEvent = collections.namedtuple("ResizeEvent", ["window", "new_size"])
KeyPressEvent = collections.namedtuple("KeyPressEvent", ["window", "key"])
KeyReleaseEvent = collections.namedtuple("KeyReleaseEvent", ["window", "key"])

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
                w, h = e.window.data1, e.window.data2
                context = weakref.ref(window._context)()
                if context:
                    context.ensure_active()
                    glViewport(0, 0, w, h)
                yield ResizeEvent(window, (w, h))
        elif e.type in _key_events and e.key.windowID in Window._all:
            event = _key_events[e.type]
            window = Window._all[e.key.windowID]
            key = str(SDL_GetKeyName(e.key.keysym.sym), "UTF-8")
            yield event(window, key)
