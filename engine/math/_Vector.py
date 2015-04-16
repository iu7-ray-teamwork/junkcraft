from . import Matrix
from math import *
from numbers import *


class Vector:
    __slots__ = ["__x", "__y"]

    zero = None
    unit_x = None
    unit_y = None

    def __init__(self, *args):
        x, y = args[0] if len(args) == 1 else args
        assert isinstance(x, Real)
        assert isinstance(y, Real)
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__,
                                   repr(self.__x), repr(self.__y))

    def __getitem__(self, i):
        return (self.__x, self.__y)[i]

    def __len__(self):
        return 2

    def __iter__(self):
        return iter((self.__x, self.__y))

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def length2(self):
        return self.__x ** 2 + self.__y ** 2

    @property
    def length(self):
        return sqrt(self.length2)

    @property
    def unit(self):
        l = self.length
        return Vector(self.__x / l, self.__y / l)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplementedError
        return self.__x == other.__x and self.__y == other.__y

    def __ne__(self, other):
        if not isinstance(other, Vector):
            return NotImplementedError
        return not (self == other)

    def __pos__(self):
        return Vector(+self.__x, +self.__y)

    def __neg__(self):
        return Vector(-self.__x, -self.__y)

    def __add__(self, other):
        return Vector(self.__x + other.__x, self.__y + other.__y)

    def __sub__(self, other):
        return Vector(self.__x - other.__x, self.__y - other.__y)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(self.__x * other, self.__y * other)
        if isinstance(other, Matrix):
            x = self.__x * other[0, 0] + self.__y * other[1, 0] + other[2, 0]
            y = self.__x * other[0, 1] + self.__y * other[1, 1] + other[2, 1]
            s = self.__x * other[0, 2] + self.__y * other[1, 2] + other[2, 2]
            return Vector(x / s, y / s)
        assert False

    def __rmul__(self, other):
        return Vector(other * self.__x, other * self.__y)

    def __truediv__(self, other):
        return Vector(self.__x / other, self.__y / other)

    def __floordiv__(self, other):
        return Vector(self.__x // other, self.__y // other)

    def dot(self, other):
        return self.__x * other.__x + self.__y * other.__y

    def cross(self, other):
        return self.__x * other.__y - self.__y * other.__x

Vector.zero = Vector(0, 0)
Vector.unit_x = Vector(1, 0)
Vector.unit_y = Vector(0, 1)
