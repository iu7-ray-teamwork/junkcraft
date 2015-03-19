import math
from numbers import Number

class Matrix:
    __slots__ = ["_values", "_size"]

    def __init__(self, list=None):
        self._size = (3, 2)
        if list is None:
            self._values = [
                [1, 0],
                [0, 1],
                [0, 0]
            ]
        else:
            if self._is_not_valid_list(list):
                raise ValueError
            self._values = list

    @property
    def size(self):
        return self._size

    @staticmethod
    def _is_not_valid_list(l):
        if len(l) != 3:
            return True
        for i in l:
            if (not isinstance(i, list) or len(i) != 2):
                return True
            for j in i:
                if not isinstance(j, Number):
                    return True
        return False

    def __getitem__(self, index):
        return self._values[index[0]][index[1]]

    @staticmethod
    def translate(dx, dy):
        return Matrix([
            [1, 0],
            [0, 1],
            [dx, dy]
        ])

    @staticmethod
    def rotate(angle):
        return Matrix([
            [math.cos(angle), math.sin(angle)],
            [-math.sin(angle), math.cos(angle)],
            [0, 0]
        ])

    @staticmethod
    def scale(kx, ky):
        return Matrix([
            [kx, 0],
            [0, ky],
            [0, 0]
        ])

    def __eq__(self, other):
        for i in range(other.size[0]):
            for j in range(other.size[1]):
                if self[i, j] != other[i, j]:
                    return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __mul__(self, x):
        assert isinstance(x, Matrix)

        e00 = self[0, 0]*x[0, 0] + self[0, 1]*x[1, 0]
        e10 = self[1, 0]*x[0, 0] + self[1, 1]*x[1, 0]
        e20 = self[2, 0]*x[0, 0] + self[2, 1]*x[1, 0] + x[2, 0]
        e01 = self[0, 0]*x[0, 1] + self[0, 1]*x[1, 1]
        e11 = self[1, 0]*x[0, 1] + self[1, 1]*x[1, 1]
        e21 = self[2, 0]*x[0, 1] + self[2, 1]*x[1, 1] + x[2, 1]

        return Matrix([
            [e00, e01],
            [e10, e11],
            [e20, e21]
        ])


class Vector:
    __slots__ = ["_x", "_y"]

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Vector(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return Vector(self._x - other.x, self._y - other.y)

    def __neg__(self):
        return Vector(-self._x, -self._y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x*other.x + self.y*other.y
        if isinstance(other, Matrix):
            x = self._x*other[0, 0] + self._y*other[1, 0] + other[2, 0]
            y = self._x*other[0, 1] + self._y*other[1, 1] + other[2, 1]
            return Vector(x, y)
        if isinstance(other, Number):
            return other * self
        else:
            raise ValueError

    def __rmul__(self, other):
        assert isinstance(other, Number)
        return Vector(self._x * other, self._y * other)

    def __truediv__(self, other):
        assert isinstance(other, Number)
        return Vector(self._x / other, self._y / other)

    @property
    def sqr_length(self):
        return self._x**2 + self._y**2

    @property
    def length(self):
        return math.sqrt(self.sqr_length)

    @property
    def normalized(self):
        l = self.length
        return Vector(self._x/l, self._y/l)
