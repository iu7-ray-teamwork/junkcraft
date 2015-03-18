import math

class Matrix:
    def __init__(self, list=None):
        if list is None:
            self._values = [
                [0, 0],
                [0, 0],
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
                if not isinstance(j, (int, float, complex)):
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
        angle = angle / 180 * math.pi
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
        return not self == other

    def __mul__(self, x):
        r = Matrix()
        r[0][0] = self[0][0]*x[0][0] + self[0][1]*x[1][0]
        r[1][0] = self[1][0]*x[0][0] + self[1][1]*x[1][0]
        r[2][0] = self[2][0]*x[0][0] + self[2][1]*x[1][0] + x[2][0]
        r[0][1] = self[0][0]*x[0][1] + self[0][1]*x[1][1]
        r[1][1] = self[1][0]*x[0][1] + self[1][1]*x[1][1]
        r[2][1] = self[2][0]*x[0][1] + self[2][1]*x[1][1] + x[2][1]
        return r
