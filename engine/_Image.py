__all__ = []

from ._IMG import *
from ._SDL import *

__all__ += ["Image"]
class Image:
    def __init__(self, path):
        self._surface = IMG_Load(path.encode("UTF-8"))

    def __del__(self):
        SDL_FreeSurface(self._surface)

    @property
    def size(self):
        c = self._surface.contents
        return c.w, c.h