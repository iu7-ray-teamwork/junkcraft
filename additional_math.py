import math
from numbers import Number

class Matrix:
    def __init__(self, list=None):
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
        return self._values[index]

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
        for i, list in enumerate(self._values):
            if list != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __mul__(self, x):
        r = Matrix()
        r[0][0] = self[0][0]*x[0][0] + self[0][1]*x[1][0]
        r[1][0] = self[1][0]*x[0][0] + self[1][1]*x[1][0]
        r[2][0] = self[2][0]*x[0][0] + self[2][1]*x[1][0] + x[2][0]
        r[0][1] = self[0][0]*x[0][1] + self[0][1]*x[1][1]
        r[1][1] = self[1][0]*x[0][1] + self[1][1]*x[1][1]
        r[2][1] = self[2][0]*x[0][1] + self[2][1]*x[1][1] + x[2][1]
        return r


class Vector:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            x = self.x*other[0][0] + self.y*other[1][0] + other[2][0]
            y = self.x*other[0][1] + self.y*other[1][1] + other[2][1]
            return Vector(x, y)
        if isinstance(other, Number):
            return other * self
        else:
            raise ValueError

    def __rmul__(self, other):
        assert isinstance(other, Number)
        return Vector(self.x * other, self.y * other)

    @property
    def sqr_length(self):
        return self.x**2 + self.y**2

    @property
    def length(self):
        return math.sqrt(self.sqr_length)

    @property
    def normalized(self):
        l = self.length
        return Vector(self.x/l, self.y/l)
