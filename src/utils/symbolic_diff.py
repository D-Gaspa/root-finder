import sympy as sp


def parse_expression(expr_str, variable):
    """
    Convert a string expression into a SymPy expression.

    Args:
    - expr_str (str): The mathematical expression as a string.
    - variable (str): The variable used in the expression.

    Returns:
    - sp.Expr: The parsed SymPy expression.
    """
    var = sp.symbols(variable)
    return sp.sympify(expr_str), var


def compute_derivative(expr_str, variable='x'):
    """
    Compute the derivative of an expression with respect to a given variable.

    Args:
    - expr_str (str): The mathematical expression as a string.
    - variable (str, optional): The variable used in the expression. Defaults to 'x'.

    Returns:
    - str: The derivative of the expression.
    """
    expr, var = parse_expression(expr_str, variable)
    derivative = sp.diff(expr, var)
    # Simplify the expression
    simplified_derivative = sp.simplify(derivative)
    return str(simplified_derivative)
