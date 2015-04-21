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
        (v1, v1, True),
        (v1, v2, False),
    ])
    def test___eq__(self, v1, v2, eq):
        assert (v1[0] == v2[0]) == eq

    @pytest.mark.parametrize('v1,v2,ne', [
        (v1, v1, False),
        (v1, v2, True)
    ])
    def test___ne__(self, v1, v2, ne):
        assert (v1[0] != v2[0]) == ne
