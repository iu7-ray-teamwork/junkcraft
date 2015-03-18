import pytest

import additional_math

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
    ( 90, [[0, 1],[-1, 0], [0, 0]] ),
    ( 360, [[1, 0],[0, 1], [0, 0]] ),
    ( 180, [[-1, 0],[0, -1], [0, 0]] ),
    ( 270, [[0, -1],[1, 0], [0, 0]] )
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
