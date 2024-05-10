import math

import pytest

from src.algorithms.modified_newton import modified_newton
from src.utils.function_evaluation import get_function_and_derivatives


def test_modified_newton_typical_case():
    f, df, ddf = get_function_and_derivatives("x**2 - 1")
    root, _ = modified_newton(f, df, ddf, 0.5)
    assert math.isclose(root, 1, rel_tol=1e-5)


def test_modified_newton_root_at_boundary():
    f, df, ddf = get_function_and_derivatives("x - 2")
    root, _ = modified_newton(f, df, ddf, 1.5)
    assert math.isclose(root, 2, rel_tol=1e-5)


def test_modified_newton_multiple_roots():
    f, df, ddf = get_function_and_derivatives("x**3 - 6*x**2 + 9*x")
    root, _ = modified_newton(f, df, ddf, 2.5)
    assert math.isclose(root, 3, rel_tol=1e-3)


def test_modified_newton_no_roots():
    f, df, ddf = get_function_and_derivatives("x**2 + 1")
    with pytest.raises(ValueError) as exif:
        modified_newton(f, df, ddf, 1)
    assert "Denominator became zero." in str(exif.value)


def test_modified_newton_non_convergence():
    f, df, ddf = get_function_and_derivatives("sin(1/x)")
    with pytest.raises(ValueError) as exif:
        modified_newton(f, df, ddf, 0.5, max_iter=3)
    assert "Exceeded maximum iterations" in str(exif.value)


def test_modified_newton_small_tolerance():
    f, df, ddf = get_function_and_derivatives("x**2 - 2")
    root, _ = modified_newton(f, df, ddf, 1.5, tol=1e-10)
    assert math.isclose(root, math.sqrt(2), rel_tol=1e-10)


def test_modified_newton_large_inputs():
    f, df, ddf = get_function_and_derivatives("1e6*x - 1e6")
    root, _ = modified_newton(f, df, ddf, 0.5, max_iter=1000)
    assert math.isclose(root, 1, rel_tol=1e-3)


if __name__ == "__main__":
    pytest.main([__file__])
