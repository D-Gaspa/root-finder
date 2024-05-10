import math

import pytest

from src.algorithms.secant import secant
from src.utils.function_evaluation import get_function


def test_secant_typical_case():
    f = get_function("x**2 - 1")
    root, _ = secant(f, -0.6, 0.5)
    assert math.isclose(root, 1, rel_tol=1e-5)


def test_secant_multiple_roots():
    f = get_function("x**3 - 6*x**2 + 9*x")
    root, _ = secant(f, 2, 3)
    assert math.isclose(root, 3, rel_tol=1e-3)


def test_secant_same_function_values():
    f = get_function("x**2 - 4")
    with pytest.raises(ValueError) as exif:
        secant(f, 2, -2)
    assert "Function values of the two guesses are the same" in str(exif.value)


def test_secant_denominator_zero():
    f = get_function("x**2 - 4")

    # Intentionally choosing initial guesses with identical function values
    try:
        secant(f, 3, 3)
    except ValueError as e:
        # Checking the actual error message
        assert str(e) == "Function values of the two guesses are the same, causing division by zero."


def test_secant_non_convergence():
    f = get_function("sin(1/x)")
    with pytest.raises(ValueError) as exif:
        secant(f, 0.25, 0.5, max_iter=3)
    assert "Exceeded maximum iterations" in str(exif.value)


def test_secant_small_tolerance():
    f = get_function("x**2 - 2")
    root, _ = secant(f, 1, 1.5, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


def test_secant_large_inputs():
    f = get_function("1e6*x - 1e6")
    root, _ = secant(f, 0, 1)
    assert math.isclose(root, 1, rel_tol=1e-3)


def test_secant_small_intervals():
    f = get_function("x**2 - 2")

    # Setting two initial guesses very close to the root
    x0 = math.sqrt(2) - 1e-5
    x1 = math.sqrt(2) + 1e-5

    root, _ = secant(f, x0, x1, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


if __name__ == "__main__":
    pytest.main([__file__])
