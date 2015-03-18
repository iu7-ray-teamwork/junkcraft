import pytest
import additional_math
import math

# Matrix tests
@pytest.mark.parametrize("input,expected", [
    ([[0, 0], [0, 0], [0, 0]], True),
    ([[0], [0], [0]], False),
    ([[0, 0], [0], [0, 0]], False),
    ([0, [0, 0], 0, 0], False),
    ([0, 0, 0], False),
    ([(0, 0), [0, 0], [0, 0]], False),
    ([0, [0, [1, 1]], 0, 0], False),
    ([[0, 0], [[0], 0], [0, 0]], False),
    ([[0, 0], ["0", 0], [0, 0]], False)
])
def test_matrix_init_with_list(input, expected):
    r = True
    try:
        m = additional_math.Matrix(input)
    except ValueError:
        r = False
    assert r == expected


@pytest.mark.parametrize("input,expected", [
    ( (3, 4), [[1, 0], [0, 1], [3, 4]] )
])
def test_matrix_translate(input, expected):
    r = additional_math.Matrix.translate(*input)
    r = [r[0], r[1], r[2]]
    assert r == expected


@pytest.mark.parametrize("input,expected", [
    ( math.pi/2, [[0, 1],[-1, 0], [0, 0]] ),
    ( math.pi*2, [[1, 0],[0, 1], [0, 0]] ),
    ( math.pi, [[-1, 0],[0, -1], [0, 0]] ),
    ( 3*math.pi/2, [[0, -1],[1, 0], [0, 0]] )
])
def test_matrix_rotate(input, expected):
    m = additional_math.Matrix.rotate(input)
    for i in range(3):
        for j in range(2):
            assert abs(expected[i][j] - m[i][j]) <= 1e-5


@pytest.mark.parametrize("input,expected", [
    ( (2, 2), [[2, 0],[0, 2],[0, 0]] )
])
def test_matrix_scale(input, expected):
    r = additional_math.Matrix.scale(*input)
    r = [r[0], r[1], r[2]]
    assert r == expected


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Matrix([[1, 2], [3, 4], [5, 6]]),
       additional_math.Matrix([[1, 2], [3, 4], [5, 6]])),
       True ),
    ( (additional_math.Matrix([[1, 2], [3, 4], [5, 6]]),
       additional_math.Matrix([[0, 2], [3, 4], [5, 6]])),
       False ),
])
def test_matrix_equality(input, expected):
    assert (input[0] == input[1]) == expected


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Matrix([[1, 2], [3, 4], [5, 6]]),
       additional_math.Matrix([[1, 2], [3, 4], [5, 6]])),
       False ),
    ( (additional_math.Matrix([[1, 2], [3, 4], [5, 6]]),
       additional_math.Matrix([[0, 2], [3, 4], [5, 6]])),
       True ),
])
def test_matrix_not_equality(input, expected):
    assert (input[0] != input[1]) == expected


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Matrix([[1, 2], [3, 4], [5, 6]]),
       additional_math.Matrix([[1, 2], [3, 4], [5, 6]])),
       additional_math.Matrix([[7, 10], [15, 22], [28, 40]])
    )
])
def test_matrix_mul(input, expected):
    r = input[0]*input[1] == expected
    assert r


#Vector tests
def test_vector_init():
    v = additional_math.Vector(10, 11)
    assert v.x == 10 and v.y == 11


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(10, 10)),
       True ),
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(11, 10)),
       False ),
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(10, 11)),
       False ),

])
def test_vector_equality(input, expected):
    assert (input[0] == input[1]) == expected

@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(10, 10)),
       False ),
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(11, 10)),
       True ),
    ( (additional_math.Vector(10, 10),
       additional_math.Vector(10, 11)),
       True ),

])
def test_vector_not_equality(input, expected):
    assert (input[0] != input[1]) == expected


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Vector(1, 2),
       additional_math.Vector(3, 4)),
       additional_math.Vector(4, 6) ),
    ( (additional_math.Vector(1, 2),
       additional_math.Vector(-3, 4)),
       additional_math.Vector(-2, 6) ),

])
def test_vector_add(input, expected):
    assert (input[0] + input[1]) == expected


@pytest.mark.parametrize("input,expected", [
    ( (additional_math.Vector(1, 2),
       10),
       additional_math.Vector(10, 20) ),
    ( (additional_math.Vector(7, 8),
       additional_math.Matrix([[1, 2], [3, 4], [5, 6]])),
       additional_math.Vector(36, 52) ),

])
def test_vector_mul(input, expected):
    assert (input[0] * input[1]) == expected


@pytest.mark.parametrize("input,expected", [
    ( additional_math.Vector(3, 4), 25 )
])
def test_vector_sqr_length(input, expected):
    assert input.sqr_length == expected


@pytest.mark.parametrize("input,expected", [
    ( additional_math.Vector(3, 4), 5 )
])
def test_vector_length(input, expected):
    assert input.length == expected


@pytest.mark.parametrize("input,expected", [
    ( additional_math.Vector(3, 5), 1 ),
    ( additional_math.Vector(2, 1), 1 ),
])
def test_vector_normalized(input, expected):
    v = input.normalized
    assert abs(v.length - expected) <= 1e-7
