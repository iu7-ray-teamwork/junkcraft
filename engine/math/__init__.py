"""Init math

"""

from math import *

from ._Matrix import *
from ._Vector import *


def clamp(a, x, b):
    if x < a:
        return a
    if x > b:
        return b
    return x
