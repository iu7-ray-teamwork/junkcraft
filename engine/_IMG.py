__all__ = []

from ._SDL import *

from sdl2.sdlimage import *
from sdl2.sdlimage import __all__ as all
__all__ += all

IMG_Init(IMG_INIT_PNG)
