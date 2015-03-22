__all__ = []

from weakref import *
from ctypes import *

from ._sdl import *
from ._Context import *

class WindowMeta(type):
    @property
    def list(cls):
        return list(cls._all.values())

__all__ += ["Window"]
class Window(metaclass=WindowMeta):
    _all = WeakValueDictionary()

    def __init__(self, **parameters):
        self._window = window = SDL_CreateWindow(
            b'',
            SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
            0, 0,
            SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE
        )

        self.__context = lambda: None

        self.title = parameters.pop("title", "")
        self.size = parameters.pop("size", (800, 600))
        self.visible = parameters.pop("visible", True)

        Window._all[SDL_GetWindowID(self._window)] = self

        def cleanup(_):
            SDL_DestroyWindow(window)
        self.__weakself = ref(self, cleanup)

    @property
    def _context(self):
        context = self.__context()
        if context is None:
            context = Context(self)
            self.__context = ref(context)
        return context

    @property
    def title(self):
        return str(SDL_GetWindowTitle(self._window), "UTF-8")

    @title.setter
    def title(self, title):
        SDL_SetWindowTitle(self._window, title.encode("UTF-8"))

    @property
    def size(self):
        w, h = c_int(), c_int()
        SDL_GetWindowSize(self._window, w, h)
        return w.value, h.value

    @size.setter
    def size(self, size):
        w, h = size
        SDL_SetWindowSize(self._window, w, h)

    @property
    def is_visible(self):
        return self.__is_visible

    @is_visible.setter
    def is_visible(self, is_visible):
        if is_visible:
            SDL_ShowWindow(self._window)
        else:
            SDL_HideWindow(self._window)
        self.__is_visible = is_visible
