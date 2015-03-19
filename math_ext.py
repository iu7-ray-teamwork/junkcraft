import numbers as _numbers

from math import *


def _cut3(m, i, j):
    return tuple(tuple(m[ii][jj] for jj in range(3) if jj != j) for ii in range(3) if ii != i)


def _det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _minor3(m, i, j):
    return _det2(_cut3(m, i, j))


def _cofactor3(m, i, j):
    return _minor3(m, i, j) * (+1, -1)[(i + j) % 2]


def _cofactors3(m):
    return tuple(tuple(_cofactor3(m, i, j) for j in range(3)) for i in range(3))


def _det_from_cofactors3(m, cf):
    return sum(mr[0] * cfr[0] for mr, cfr in zip(m, cf))


def _trans3(m):
    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def _inv3(m):
    cf = _cofactors3(m)
    d = _det_from_cofactors3(m, cf)
    return tuple(tuple(e / d for e in r) for r in _trans3(cf))


class Matrix:
    __slots__ = ["__rows"]

    def __init__(self, *rows):
        assert len(rows) == 3
        for i, row in enumerate(rows):
            assert type(row) == tuple
            assert len(row) == 3
            for j, element in enumerate(row):
                assert isinstance(element, _numbers.Real)
        self.__rows = rows

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, *self.__rows)

    @staticmethod
    def translate(dx, dy):
        return Matrix(
            ( 1,  0,  0),
            ( 0,  1,  0),
            (dx, dy,  1)
        )

    @staticmethod
    def rotate(angle):
        s = sin(angle)
        c = cos(angle)
        return Matrix(
            ( c, +s,  0),
            (-s,  c,  0),
            (0,   0,  1)
        )

    @staticmethod
    def scale(kx, ky):
        return Matrix(
            (kx,  0,  0),
            ( 0, ky,  0),
            ( 0,  0,  1)
        )

    def __getitem__(self, ij):
        i, j = ij
        assert 0 <= i <= 2
        assert 0 <= j <= 2
        return self.__rows[i][j]

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplementedError
        return self.__rows == other.__rows

    def __ne__(self, other):
        if not isinstance(other, Matrix):
            return NotImplementedError
        return not (self == other)

    def __invert__(self):
        return Matrix(*_inv3(self.__rows))

    def __mul__(self, other):
        a, b = self.__rows, other.__rows
        r = [[None] * 3] * 3
        for i in range(3):
            for j in range(3):
                r[i][j] = sum(a[i][k] * b[k][j] for k in range(3))
            r[i] = tuple(r[i])
        return Matrix(*r)


Matrix.zero = Matrix(
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0)
)

Matrix.identity = Matrix(
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1)
)


class Vector:
    __slots__ = ["__x", "__y"]

    def __init__(self, x, y):
        assert isinstance(x, _numbers.Real)
        assert isinstance(y, _numbers.Real)
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.__x, self.__y)

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __getitem__(self, i):
        if i == 0:
            return self.__x
        if i == 1:
            return self.__y
        assert False

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def length2(self):
        return self.__x*self.__x + self.__y*self.__y

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
        if isinstance(other, _numbers.Number):
            return Vector(self.__x * other, self.__y * other)
        if isinstance(other, Matrix):
            x = self.__x*other[0, 0] + self.__y*other[1, 0] + other[2, 0]
            y = self.__x*other[0, 1] + self.__y*other[1, 1] + other[2, 1]
            s = self.__x*other[0, 2] + self.__y*other[1, 2] + other[2, 2]
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
