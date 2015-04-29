import pytest
from engine.math import Vector


v1 = (Vector(3, 4), 3, 4, 5, 1)
v2 = (Vector(4, 4), 4, 4, 5.656854249492381, 1)
vector_str = 'v,x,y,length,unit'
parametrize_vector = (vector_str, [v1, v2])


class TestVector:
    @pytest.mark.parametrize(*parametrize_vector)
    def test_x(self, v, x, y, length, unit):
        assert v.x == x

    @pytest.mark.parametrize(*parametrize_vector)
    def test_y(self, v, x, y, length, unit):
        assert v.y == y

    @pytest.mark.parametrize(*parametrize_vector)
    def test_length(self, v, x, y, length, unit):
        assert v.length == length

    @pytest.mark.parametrize(*parametrize_vector)
    def test_unit(self, v, x, y, length, unit):
        assert v.unit == unit

    @pytest.mark.parametrize('v1,v2,eq', [
        (v1[0], v1[0], True),
        (v1[0], v2[0], False),
    ])
    def test___eq__(self, v1, v2, eq):
        assert (v1 == v2) == eq

    @pytest.mark.parametrize('v1,v2,ne', [
        (v1[0], v1[0], False),
        (v1[0], v2[0], True)
    ])
    def test___ne__(self, v1, v2, ne):
        assert (v1 != v2) == ne

    @pytest.mark.parametrize('v1,v2,mul', [
        (v1[0], 3, Vector(9, 12)),
        (v1[0], v2[0], Vector(12, 16))
    ])
    def test___mul__(self, v1, v2, mul):
        assert v1*v2 == mul

    @pytest.mark.parametrize('v1,v2,mul', [
        (    3, v1[0], Vector(9, 12)),
        (v2[0], v1[0], Vector(12, 16))
    ])
    def test___mul__(self, v1, v2, mul):
        assert v1*v2 == mul

    @pytest.mark.parametrize('v1,v2,mul', [
        (v1[0],     3, Vector(9, 12)),
        (v1[0], v2[0], Vector(12, 16))
    ])
    def test___rmul__(self, v1, v2, mul):
        assert v1*v2 == mul

    @pytest.mark.parametrize('v1,v2,div', [
        (v1[0],     3, Vector(1, 4/3)),
        (v1[0], v2[0], Vector(3/4, 1))
    ])
    def test___truediv__(self, v1, v2, div):
        assert v1/v2 == div

    @pytest.mark.parametrize('v1,v2,div', [
        (v1[0],     3, Vector(1, 1)),
        (v1[0], v2[0], Vector(0, 1))
    ])
    def test___floordiv__(self, v1, v2, div):
        assert v1//v2 == div


