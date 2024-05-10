import math

import pytest

from src.algorithms.newton import newton
from src.utils.function_evaluation import get_function_and_derivatives


def test_newton_typical_case():
    # A simple quadratic function with a root between -1 and 1
    f, df, _ = get_function_and_derivatives("x**2 - 1")
    root, _ = newton(f, df, 0.5)
    assert math.isclose(root, 1, rel_tol=1e-5)


def test_newton_root_at_boundary():
    # A simple linear function with a root at x=2
    f, df, _ = get_function_and_derivatives("x - 2")
    root, _ = newton(f, df, 1.5)
    assert math.isclose(root, 2, rel_tol=1e-5)


def test_newton_multiple_roots():
    # A function with multiple roots
    f, df, _ = get_function_and_derivatives("x**3 - 6*x**2 + 9*x")
    root, _ = newton(f, df, 2.5)
    assert math.isclose(root, 3, rel_tol=1e-3)


def test_newton_no_roots():
    f, df, _ = get_function_and_derivatives("x**2 + 1")
    with pytest.raises(ValueError) as exif:
        newton(f, df, 1)
    assert "Derivative is zero. Cannot continue iteration." in str(exif.value)


def test_newton_derivative_zero_initial_guess():
    f, df, _ = get_function_and_derivatives("x**2")
    with pytest.raises(ValueError) as exif:
        newton(f, df, 0)
    assert "Derivative is zero at the initial guess." in str(exif.value)


def test_newton_non_convergence():
    f, df, _ = get_function_and_derivatives("sin(1/x)")
    with pytest.raises(ValueError) as exif:
        newton(f, df, 0.5, max_iter=3)
    assert "Exceeded maximum iterations" in str(exif.value)


def test_newton_small_tolerance():
    f, df, _ = get_function_and_derivatives("x**2 - 2")
    root, _ = newton(f, df, 1.5, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


def test_newton_large_inputs():
    f, df, _ = get_function_and_derivatives("1e6*x - 1e6")
    root, _ = newton(f, df, 0.5, max_iter=1000)
    assert math.isclose(root, 1, rel_tol=1e-3)


if __name__ == "__main__":
    pytest.main([__file__])
