import pytest
from engine.math import Vector


@pytest.mark.parametrize('v,x,y', [
    (Vector(3, 4), 3, 4)
])
class TestVector:
    @staticmethod
    def test_x(v, x, y):
        assert v.x == x
