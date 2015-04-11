__all__ = []

from weakref import *

from ._SDL import *

__all__ += ["Context"]
class Context:
    def __init__(self, window):
        self.__window = window

        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        self.__context = context = SDL_GL_CreateContext(self.__window._window)

        def cleanup(_):
            SDL_GL_DeleteContext(context)
        self.__weakself = ref(self, cleanup)

    def ensure_active(self):
        SDL_GL_MakeCurrent(self.__window._window, self.__context)




