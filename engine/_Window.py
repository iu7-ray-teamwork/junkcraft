import weakref
from ctypes import *

from ._SDL import *
from . import math


class _Context:
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)

    def __init__(self, window):
        self.window = window

        self.handle = handle = SDL_GL_CreateContext(self.window._handle)

        def cleanup(_):
            SDL_GL_DeleteContext(handle)
        self.__weakself = weakref.ref(self, cleanup)

    def ensure_active(self):
        SDL_GL_MakeCurrent(self.window._handle, self.handle)


class _WindowMeta(type):
    @property
    def list(cls):
        return list(cls._all.values())


class Window(metaclass=_WindowMeta):
    _all = weakref.WeakValueDictionary()

    def __init__(self, **parameters):
        self._handle = handle = SDL_CreateWindow(
            b'',
            SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
            0, 0,
            SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)

        self.__context = lambda: None

        self.title = parameters.pop("title", "")
        self.size = parameters.pop("size", (800, 600))
        self.visible = parameters.pop("visible", True)

        Window._all[SDL_GetWindowID(self._handle)] = self

        def cleanup(_):
            SDL_DestroyWindow(handle)
        self.__weakself = weakref.ref(self, cleanup)

    @property
    def _context(self):
        context = self.__context()
        if context is None:
            context = _Context(self)
            self.__context = weakref.ref(context)
        return context

    @property
    def title(self):
        return str(SDL_GetWindowTitle(self._handle), "UTF-8")

    @title.setter
    def title(self, title):
        SDL_SetWindowTitle(self._handle, title.encode("UTF-8"))

    @property
    def size(self):
        w, h = c_int(), c_int()
        SDL_GetWindowSize(self._handle, w, h)
        return math.Vector(w.value, h.value)

    @size.setter
    def size(self, size):
        w, h = size
        SDL_SetWindowSize(self._handle, w, h)

    @property
    def is_visible(self):
        return self.__is_visible

    @is_visible.setter
    def is_visible(self, is_visible):
        if is_visible:
            SDL_ShowWindow(self._handle)
        else:
            SDL_HideWindow(self._handle)
        self.__is_visible = is_visible
