from ._SDL import *


class Surface:
    def __init__(self, window):
        self.__window = window
        self._context = window._context

    def commit(self):
        self._context.ensure_active()
        SDL_GL_SwapWindow(self.__window._window)
