"""The module handle math matrix structure and operations with them.

"""

from numbers import *
from math import *


class Matrix:
    """This class implements mathematical matrix with 3 columns and 3 rows.

    The class implements basic matrix operations used for representation
    objects in 2D space like translate, rotate or scale. The class provides
    basic matrix operations like determinant, minor, transpose, cofactor also.

    Attributes:
        zero (Matrix): A matrix with all zero elements.
        identity (Matrix): A matrix with all ones on main diagonal.

    """

    __slots__ = ["__rows"]

    zero = None
    identity = None

    def __init__(self, *rows):
        """Creates new matrix.

        Args:
            rows(tuple of tuples of float): Tuple contain tuples wich represent
                rows of the matrix by element.

                Example:
                    Tuple
                    (
                        (1, 2, 3),
                        (4, 5, 6),
                        (7, 8, 9)
                    )
                    Represent Matrix with row #0 as (1, 2, 3), row #1 as
                    (4, 5, 6) and row #2 as (7, 8, 9). It means that first
                    element of the matrix with indexes (0,0) is 1self.

        Raises:
            AssertationError: if bad tuple format of rows is given.

        """

        assert len(rows) == 3
        for i, row in enumerate(rows):
            assert row.__class__ == tuple
            assert len(row) == 3
            for j, element in enumerate(row):
                assert isinstance(element, Real)
        self.__rows = rows

    def __repr__(self):
        """Represent matrix in string format

        Returns:
            (str): Matrix in string format

        """

        return "{}({})".format(self.__class__.__name__, ', '.join(map(repr, self.__rows)))

    @staticmethod
    def translate(*args):
        """Creates a translation matrix.

        Args:
            args(tuple or float): If the float was given then offset by
                x-axis and y-axis supoose the same and equal to the float value.
                If the tuple was given then x-axis offset equals to first
                element of the tuple and y-axis offset to second element of the
                tuple.

        Returns:
            (Matrix): Matrix with translation operation.

        """

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
    def rotate(angle):
        """Creates rotation matrix.

        Args:
            angle(float): Angle of rotation (counterclockwised)

        Returns:
            (Matrix): Matrix with rotation operation.

        """

        s = sin(angle)
        c = cos(angle)
        return Matrix(
            ( c, +s,  0),
            (-s,  c,  0),
            ( 0,  0,  1)
        )

    @staticmethod
    def scale(*args):
        """Creates scale matrix

        Args:
            args(tuple of float or float)

        Returns:
            (Matrix): Scale matrix with two scale factors (for x and y axes
                respectively) or one factor if number instead of tuple was
                ginen by args.
        """

        if len(args) == 1:
            try:
                fx, fy = args[0]
            except TypeError:
                fx, fy = args[0], args[0]
        else:
            fx, fy = args
        return Matrix(
            (fx,  0,  0),
            ( 0, fy,  0),
            ( 0,  0,  1)
        )

    def __getitem__(self, ij):
        """Access to elemnt of the matrix

        Args:
            ij(tuple of int): tuple containig indexes i and j respectively.

        Returns:
            (float): Element of the matrix by row at index i and column at j

        """
        i, j = ij
        assert 0 <= i <= 2
        assert 0 <= j <= 2
        return self.__rows[i][j]

    @property
    def translation_delta(self):
        """Calculate translation delta of the matrix.

        Retruns:
            (Vector): The vector coresponding translation.

        """

        from ._Vector import Vector
        dx, dy = self[2, 0], self[2, 1]
        return Vector(dx, dy)

    @property
    def rotation_angle(self):
        """Calculate angle of the matrix.

        Retruns:
            (Vector): Angle of rotation of the matrix.

        """
        s, c = self[0, 1], self[0, 0]
        return atan2(s, c)

    @property
    def scaling_factor(self):
        """Calculating scaling factor of the matrix.

        Returns:
            (Vector): The vector wich has kx and ky scaling factors in his x, y
                components respectively.

        """

        from ._Vector import Vector
        a, b = self[0, 0], self[0, 1]
        c, d = self[1, 0], self[1, 1]
        kx = copysign(sqrt(a ** 2 + c ** 2), a)
        ky = copysign(sqrt(b ** 2 + d ** 2), d)
        return Vector(kx, ky)

    def __eq__(self, other):
        """'Equals' operation for the matricies.

        Args:
            other(Matrix): other matrix for comparsion

        Returns:
            (bool): If matricies are equal element by element.
            (NotImplemented): if other is not an instance of Matrix class.

        """

        if not isinstance(other, Matrix):
            return NotImplementedError
        return self.__rows == other.__rows

    def __ne__(self, other):
        """'Not equals' operation for the matricies.

        Args:
            other(Matrix): other matrix for comparsion

        Returns:
            (bool): If matricies are not equal element by element.
            (NotImplemented): if other is not an instance of Matrix class.

        """

        if not isinstance(other, Matrix):
            return NotImplementedError
        return not (self == other)

    def __invert__(self):
        """Invert the matrix.

        Returns:
            (Matrix): Inverted matrix.
        """

        return Matrix(*_inverse3(self.__rows))

    def __mul__(self, other):
        """Multiple two matrix.

        Args:
            other(Matrix): The multiplier.

        Returns:
            (Matrix): Product of two matricies.

        """

        a, b = self.__rows, other.__rows
        r = [[None] * 3] * 3
        for i in range(3):
            for j in range(3):
                r[i][j] = sum(a[i][k] * b[k][j] for k in range(3))
            r[i] = tuple(r[i])
        return Matrix(*r)

    def about(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args
        return Matrix.translate(-x, -y) * self * Matrix.translate(+x, +y)

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
    """
    """
    from . import Vector
    if origin is not None:
        origin = Vector(origin)
        m = Matrix.translate(-origin) * m * Matrix.translate(origin)
    return m


def _cut3(m, i, j):
    """Buld matrix without i row and j column.

    Args:
        m(tuple of tuple of floats): The matrix.
        i(int): Excluding row.
        j(int): Excluding column.

    Returns:
        (tuple of tuple of floats): Matrix without i row and j column.

    """

    return tuple(tuple(m[ii][jj] for jj in range(3) if jj != j) for ii in range(3) if ii != i)


def _determinant2(m):
    """ Calculate the determinant of matrix with 2x2 size.

    Args:
        m(tuple of tuple of float): 2x2 matrix.

    Returns:
        (float): deteriminant of given m matrix.

    """
        m(tuple of tuple of float):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _minor3(m, i, j):
    """Calculate minor of the matrix.

    Args:
        m(tuple of tuple of float): The matrix.
        i(int): Row of the minor.
        j(int): Column of the minor.

    Returns:
        (float): Minor of the matrix.
    """

    return _determinant2(_cut3(m, i, j))


def _cofactor3(m, i, j):
    """Calculate cofactor of the matrix.

    Args:
        m(tuple of tuple of float): The matrix.
        i(int): Row of the cofactor.
        j(int): Column of the cofactor.

    Retruns:
        (float): Cofactor of the matrix.

    """

    return _minor3(m, i, j) * (+1, -1)[(i + j) % 2]


def _cofactors3(m):
    """Calculate all cofactors of the matrix.

    Args:
        m(tuple of tuple of float): The matrix.

    Retruns:
        (tuple of tuple of float): The matrix of cofactors.

    """
    return tuple(tuple(_cofactor3(m, i, j) for j in range(3)) for i in range(3))


def _determinant_from_cofactors3(m, cf):
    """Calculate determinant of the matrix from cofactors.

    Args:
        m(tuple of tuple of float): The matrix.
        cf(tuple of tuple of float): The cofactors matrix.

    Returns:
        (float): Determinant.

    """

    return sum(mr[0] * cfr[0] for mr, cfr in zip(m, cf))


def _transpose3(m):
    """Transpose the matrix.

    Args:
        m(tuple of tuple of float): The matrix.

    Returns:
        (tuple of tuple of float): Transposed matrix.

    """

    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def _inverse3(m):
    """Invert the matrix.

    Args:
        m(tuple of tuple of float): the matrix.

    Returns:
        (tuple of tuple of float): Inverted matrix.

    """

    cf = _cofactors3(m)
    d = _determinant_from_cofactors3(m, cf)
    return tuple(tuple(e / d for e in r) for r in _transpose3(cf))
