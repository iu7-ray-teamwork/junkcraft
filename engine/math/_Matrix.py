from numbers import *
from math import *


class Matrix:
    __slots__ = ["__rows"]

    zero = None
    identity = None

    def __init__(self, *rows):
        assert len(rows) == 3
        for i, row in enumerate(rows):
            assert row.__class__ == tuple
            assert len(row) == 3
            for j, element in enumerate(row):
                assert isinstance(element, Real)
        self.__rows = rows

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ', '.join(map(repr, self.__rows)))

    @staticmethod
    def translate(*args, origin=None):
        if len(args) == 1:
            dx, dy = args[0]
        else:
            dx, dy = args
        return Matrix(
            ( 1,  0,  0),
            ( 0,  1,  0),
            (dx, dy,  1)
        )

    @staticmethod
    def rotate(angle, *, origin=None):
        s = sin(angle)
        c = cos(angle)
        m = Matrix(
            ( c, +s,  0),
            (-s,  c,  0),
            (0,   0,  1)
        )
        return _transform_origin(m, origin)

    @staticmethod
    def scale(*args, origin=None):
        if len(args) == 1:
            try:
                kx, ky = args[0]
            except TypeError:
                kx, ky = args[0], args[0]
        else:
            kx, ky = args
        m = Matrix(
            (kx,  0,  0),
            ( 0, ky,  0),
            ( 0,  0,  1)
        )
        return _transform_origin(m, origin)

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
        return Matrix(*_inverse3(self.__rows))

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


def _transform_origin(m, origin):
    from . import Vector
    if origin is not None:
        origin = Vector(origin)
        m = Matrix.translate(-origin) * m * Matrix.translate(origin)
    return m


def _cut3(m, i, j):
    return tuple(tuple(m[ii][jj] for jj in range(3) if jj != j) for ii in range(3) if ii != i)


def _determinant2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _minor3(m, i, j):
    return _determinant2(_cut3(m, i, j))


def _cofactor3(m, i, j):
    return _minor3(m, i, j) * (+1, -1)[(i + j) % 2]


def _cofactors3(m):
    return tuple(tuple(_cofactor3(m, i, j) for j in range(3)) for i in range(3))


def _determinant_from_cofactors3(m, cf):
    return sum(mr[0] * cfr[0] for mr, cfr in zip(m, cf))


def _transpose3(m):
    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def _inverse3(m):
    cf = _cofactors3(m)
    d = _determinant_from_cofactors3(m, cf)
    return tuple(tuple(e / d for e in r) for r in _transpose3(cf))
