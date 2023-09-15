import math
import pytest
from src.utils.function_evaluation import get_function
from src.algorithms.false_position import false_position


def test_false_position_typical_case():
    f = get_function("x**2 - 1")
    root, _ = false_position(f, 0, 2)
    assert math.isclose(root, 1, rel_tol=1e-5)


def test_false_position_root_at_boundary():
    f = get_function("x - 2")
    root, _ = false_position(f, 1, 2)
    assert math.isclose(root, 2, rel_tol=1e-5)


def test_false_position_multiple_roots():
    f = get_function("x**3 - 6*x**2 + 9*x")
    root, _ = false_position(f, 2.5, 3)
    assert math.isclose(root, 3, rel_tol=1e-5)


def test_false_position_no_roots():
    f = get_function("x + 2")
    with pytest.raises(ValueError):
        false_position(f, -1, 1)


def test_false_position_maximum_iterations():
    f = get_function("exp(-x) - x")
    with pytest.raises(ValueError) as exif:
        false_position(f, 0, 1, max_iter=2)
    assert "Exceeded maximum iterations" in str(exif.value)


def test_false_position_near_zero_change():
    f = get_function("(x - 2)**3")
    root, _ = false_position(f, 1, 3)
    assert math.isclose(root, 2, rel_tol=1e-5)


def test_false_position_large_inputs():
    f = get_function("1e6*x - 1e6")
    root, _ = false_position(f, 0, 1e6)
    assert math.isclose(root, 1, rel_tol=1e-3)


def test_false_position_small_intervals():
    f = get_function("x**2 - 2")

    # Setting a very small interval around the root
    a = math.sqrt(2) - 1e-5
    b = math.sqrt(2) + 1e-5

    root, _ = false_position(f, a, b, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


if __name__ == "__main__":
    pytest.main([__file__])
