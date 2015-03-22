__all__ = []

from OpenGL.GL import *
import OpenGL.GL
__all__ += (n for n in dir(OpenGL.GL) if n.startswith("GL") or n.startswith("gl"))
