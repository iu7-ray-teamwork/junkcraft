import collections
import weakref

from . import math
from ._SDL import *
from ._GL import *
from ._Window import *

UserQuitEvent = collections.namedtuple("UserQuitEvent", [])
ResizeEvent = collections.namedtuple("ResizeEvent", ["window", "new_size"])
KeyPressEvent = collections.namedtuple("KeyPressEvent", ["window", "key"])
KeyReleaseEvent = collections.namedtuple("KeyReleaseEvent", ["window", "key"])
MouseButtonPressEvent = collections.namedtuple("MouseButtonPressEvent", ["window", "position", "button"])
MouseButtonReleaseEvent = collections.namedtuple("MouseButtonReleaseEvent", ["window", "position", "button"])

_key_events = {
    SDL_KEYDOWN: KeyPressEvent,
    SDL_KEYUP: KeyReleaseEvent,
}

_mouse_button_events = {
    SDL_MOUSEBUTTONDOWN: MouseButtonPressEvent,
    SDL_MOUSEBUTTONUP: MouseButtonReleaseEvent,
}

_mouse_button_names = {
    SDL_BUTTON_LEFT: "Left",
    SDL_BUTTON_MIDDLE: "Wheel",
    SDL_BUTTON_RIGHT: "Right",
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
        elif e.type in _mouse_button_events and e.button.windowID in Window._all:
            event = _mouse_button_events[e.type]
            window = Window._all[e.button.windowID]
            position = math.Vector(e.button.x, e.button.y)
            button = _mouse_button_names[e.button.button]
            yield event(window, position, button)
