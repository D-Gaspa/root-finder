import math
import pytest
from src.utils.function_evaluation import get_function
from src.algorithms.bisection import bisection


def test_bisection_typical_case():
    f = get_function("x**2 - 3")
    root, iterations = bisection(f, 1, 2)
    assert math.isclose(root, (3**0.5), abs_tol=1e-5)


def test_bisection_root_at_boundary():
    f = get_function("x - 2")
    root, _ = bisection(f, 1, 2)
    assert math.isclose(root, 2, rel_tol=1e-5)


def test_bisection_multiple_roots():
    f = get_function("x**3 - 6*x**2 + 9*x")
    root, _ = bisection(f, -0.5, 0.5)
    assert math.isclose(root, 0, rel_tol=1e-5)


def test_bisection_no_roots():
    f = get_function("x + 2")
    with pytest.raises(ValueError) as exif:
        bisection(f, 1, 2)
    assert "The function does not change sign" in str(exif.value)


def test_bisection_maximum_iterations():
    f = get_function("exp(-x) - x")
    with pytest.raises(ValueError) as exif:
        bisection(f, 0, 1, max_iter=2)
    assert "Exceeded maximum iterations" in str(exif.value)


def test_bisection_near_zero_change():
    f = get_function("1e-10*x")
    root, _ = bisection(f, -1, 1)
    assert math.isclose(root, 0, abs_tol=1e-5)


def test_bisection_large_inputs():
    f = get_function("1e6*x - 1e6")
    root, _ = bisection(f, 0, 1e6)
    assert math.isclose(root, 1, rel_tol=1e-3)


def test_bisection_small_intervals():
    f = get_function("x**2 - 2")

    # Setting a very small interval around the root
    a = math.sqrt(2) - 1e-5
    b = math.sqrt(2) + 1e-5

    root, _ = bisection(f, a, b, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


if __name__ == "__main__":
    pytest.main([__file__])
