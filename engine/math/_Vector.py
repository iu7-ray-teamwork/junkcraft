from math import *
from numbers import *

from . import Matrix


class Vector:
    """Representation of mathematical vector in 2D space.

    Has x and y coordinates in space.

    Attributes:
        zero(Vector): Vector with x and y coordinates equals zero.
        unit_x(Vector): Vector with x equals one and y equals zero.
        unit_y(Vector): Vector with x equals zero and y equals one.

    """

    __slots__ = ["__x", "__y"]

    zero = None
    unit_x = None
    unit_y = None

    def __init__(self, *args):
        """Creates a new Vector instance

        Args:
            args(tuple of float or float): If args is float then x and y
                coordinates equals this numberself. Else x and y equals tuple
                components respectivelyself.

        Raises:
            AssertationError: if x or y in args tuple is not of instance of
                Real.

        """

        x, y = args[0] if len(args) == 1 else args
        assert isinstance(x, Real)
        assert isinstance(y, Real)
        self.__x = x
        self.__y = y

    def __repr__(self):
        """String representation of Vector class

        Build string representation, containing x, y coordinates and class
        name.

        """

        return "{}({}, {})".format(self.__class__.__name__, repr(self.__x), repr(self.__y))

    def __getitem__(self, i):
        """Give access to coordinates by index.

        Args:
            i(int): Index of coordinate. Index equals zero is coresponding to x
                coordinate and equals one is coresponding to y coordinate off
                the vector.

        Returns:
            (float): x or y coordinate of the vector.

        """

        return (self.__x, self.__y)[i]

    def __len__(self):
        """Length of the vector class instance

        Returns:
            (int): Is always 2

        """

        return 2

    def __iter__(self):
        """Iterator object of the vector class instance.

        Returns:
            (iterator object): Iterable x and y coodinates of the vector.

        """

        return iter((self.__x, self.__y))

    @property
    def x(self):
        """X coordinate of the vector.

        Returns:
            (float): X coordinate of vector.

        """

        return self.__x

    @property
    def y(self):
        """Y coordinate of the vector.

        Returns:
            (float): Y coordinate of vector.

        """
        return self.__y

    @property
    def length2(self):
        """Square length of the vector.

        Equals to x^2 + y^2.

        Returns:
            (float): Square length of the vector

        """
        return self.__x ** 2 + self.__y ** 2

    @property
    def length(self):
        """Length of the vector in the meaning of 2D space.

        Equals to sqrt(x^2 + y^2)

        Returns:
            (float): Length of the vector.

        """
        return sqrt(self.length2)

    @property
    def unit(self):
        """Normalize the vector.

        After operation length of the vector in space will equal one.

        Retruns:
            (float): unit vector with same direction and length equal to one.

        """

        return self / self.length

    def __eq__(self, other):
        """Equality operation with other vector.

        Args:
            other(vector): Other vector to comprasion.

        Returns:
            (bool): True if x and y equals to x and y of other vector.

        Raises:
            NotImplementedError: If other argument is not an instance of the
                vector class.

        """

        if not isinstance(other, Vector):
            return NotImplementedError
        return self.__x == other.__x and self.__y == other.__y

    def __ne__(self, other):
        """'Not equal' operation with other vector.

        Args:
            other(vector): Other vector to comprasion.

        Returns:
            (bool): True if x or y not equals to x or y of other vector.

        Raises:
            NotImplementedError: If other argument is not an instance of the
                vector class.

        """

        if not isinstance(other, Vector):
            return NotImplementedError
        return not (self == other)

    def __pos__(self):
        """Positive representation of the vector.

        Returns:
            (Vector): Vector with x and y coordinates wich are greater or equal
                zero.

        """

        return Vector(+self.__x, +self.__y)

    def __neg__(self):
        """Negative representation of the vector.

        Returns:
            (Vector): Vector with x and y coordinates wich are lesser or equal
                zero.

        """

        return Vector(-self.__x, -self.__y)

    def __add__(self, other):
        """Opertion of addition.

        Args:
            other(Vector or float): Other vector for addition or the number.

        Returns:
            (Vector): Vector with composed coordinates with other vector or
                number.
            (NotImplemented): if other not an instance of Real or Vector.

        """

        if isinstance(other, Real):
            return Vector(self.__x + other, self.__y + other)
        if isinstance(other, Vector):
            return Vector(self.__x + other.__x, self.__y + other.__y)
        return NotImplemented

    def __radd__(self, other):
        """Opertion of right addition.

        Args:
            other(Vector or float): Other vector for addition or the number.

        Returns:
            (Vector): Vector with composed coordinates with other vector or
                number.
            (NotImplemented): if other not an instance of Real or Vector.

        """

        if isinstance(other, Real):
            return Vector(other + self.__x, other + self.__y)
        if isinstance(other, Vector):
            return Vector(other.__x + self.__x, other.__y + self.__y)
        return NotImplemented

    def __sub__(self, other):
        """Opertion of substraction.

        Args:
            other(Vector or float): Other vector for substraction or the number.

        Returns:
            (Vector): Vector with substracted coordinates with other vector or
                number.
            (NotImplemented): if other not an instance of Real or Vector.

        """
        if isinstance(other, Real):
            return Vector(self.__x - other, self.__y - other)
        if isinstance(other, Vector):
            return Vector(self.__x - other.__x, self.__y - other.__y)
        return NotImplemented

    def __rsub__(self, other):
        """Opertion of right substraction.

        Args:
            other(Vector or float): Other vector for substraction or the number.

        Returns:
            (Vector): Vector with substracted coordinates with other vector or
                number.
            (NotImplemented): if other not an instance of Real or Vector.

        """
        if isinstance(other, Real):
            return Vector(other - self.__x, other - self.__y)
        if isinstance(other, Vector):
            return Vector(other.__x - self.__x, other.__y - self.__y)
        return NotImplemented

    def __mul__(self, other):
        """Opertion of multiplication.

        Args:
            other(Vector or float or Matrix): other object to multiple with.

        Returns:
            (Vector): If 'other' argument is number, then x, y coordianates
                multiple on this number. If 'other' argument is
                vector then x, y coordinates multiple with x, y coordianates
                other vector respectively. If 'other' is instance of Matrix
                then function result is multiplication vector on matrix in
                mathemtical meaning.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(self.__x * other, self.__y * other)
        if isinstance(other, Vector):
            return Vector(self.__x * other.__x, self.__y * other.__y)
        if isinstance(other, Matrix):
            x = self.__x * other[0, 0] + self.__y * other[1, 0] + other[2, 0]
            y = self.__x * other[0, 1] + self.__y * other[1, 1] + other[2, 1]
            s = self.__x * other[0, 2] + self.__y * other[1, 2] + other[2, 2]
            return Vector(x / s, y / s)
        return NotImplemented

    def __rmul__(self, other):
        """Opertion of right multiplication.

        Args:
            other(Vector or float): other object to multiple with.

        Returns:
            (Vector): If 'other' argument is number, then x, y coordianates
                multiple on this number. If 'other' argument is
                vector then x, y coordinates multiple with x, y coordianates
                other vector respectively.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(other * self.__x, other * self.__y)
        if isinstance(other, Vector):
            return Vector(other.__x * self.__x, other.__y * self.__y)
        return NotImplemented

    def __truediv__(self, other):
        """Opertion of division.

        Args:
            other(Vector or float): the divider

        Returns:
            (Vector): If 'other' argument is number, then x, y coordianates
                divide on this number. If 'other' argument is
                vector then x, y coordinates divide with x, y coordianates
                other vector respectively.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(self.__x / other, self.__y / other)
        if isinstance(other, Vector):
            return Vector(self.__x / other.__x, self.__y / other.__y)
        return NotImplemented

    def __rtruediv__(self, other):
        """Opertion of right division.

        Args:
            other(Vector or float): the dividend

        Returns:
            (Vector): If 'other' argument is number, then result is vector
                with divident divided on x and y coordinates respectively
                divide on this number. If 'other' argument is
                vector then x, y coordinates divide with x, y coordianates
                other vector respectively.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(other / self.__x, other / self.__y)
        if isinstance(other, Vector):
            return Vector(other.__x / self.__x, other.__y / self.__y)
        return NotImplemented

    def __floordiv__(self, other):
        """ Operation of floor divison.

        Args:
            other(Vector or float): the divider

        Returns:
            (Vector): If 'other' argument is number, then x, y coordianates
                divide on this number. If 'other' argument is
                vector then x, y coordinates divide with x, y coordianates
                other vector respectively. Result is Vector with
                integer coordinates.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(self.__x // other, self.__y // other)
        if isinstance(other, Vector):
            return Vector(self.__x // other.__x, self.__y // other.__y)
        return NotImplemented

    def __rfloordiv__(self, other):
        """Opertion of right floor division.

        Args:
            other(Vector or float): the dividend

        Returns:
            (Vector): If 'other' argument is number, then result is vector
                with divident divided on x and y coordinates respectively
                divide on this number. If 'other' argument is
                vector then x, y coordinates divide with x, y coordianates
                other vector respectively. Result is Vector with
                integer coordinates.
            (NotImplemented): if 'other' everything else

        """

        if isinstance(other, Real):
            return Vector(other // self.__x, other // self.__y)
        if isinstance(other, Vector):
            return Vector(other.__x // self.__x, other.__y // self.__y)
        return NotImplemented

    def dot(self, other):
        """Opertaion of the dot product two vectors.

        Args:
            (Vecotr): Other vector.

        Returns:
            (float): dot product of self with other vector

        """
        return self.__x * other.__x + self.__y * other.__y

    def cross(self, other):
        """Opertaion of the cross product two vectors.

        Args:
            (Vecotr): Other vector.

        Returns:
            (float): cross product of self with other vector

        """
        return self.__x * other.__y - self.__y * other.__x

Vector.zero = Vector(0, 0)
Vector.unit_x = Vector(1, 0)
Vector.unit_y = Vector(0, 1)
