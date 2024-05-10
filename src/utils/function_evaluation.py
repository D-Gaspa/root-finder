import math

from src.utils.symbolic_diff import compute_derivative


def get_function_and_derivatives(expr):
    """Returns the function, first derivative, and second derivative of the given expression.

    Parameters:
    - expr (str): A string representing a mathematical expression.

    Returns:
    - f (function): The function represented by the expression.
    - df (function): The first derivative of the function.
    - ddf (function): The second derivative of the function.
    """
    f_str = expr
    df_str = compute_derivative(expr)
    ddf_str = compute_derivative(df_str)

    eval_context = {"x": None}
    eval_context.update(math.__dict__)

    def f(x):
        eval_context["x"] = x
        return eval(f_str, eval_context)

    def df(x):
        eval_context["x"] = x
        return eval(df_str, eval_context)

    def ddf(x):
        eval_context["x"] = x
        return eval(ddf_str, eval_context)

    return f, df, ddf


def get_function(expr):
    """Returns the function represented by the given expression.

    Parameters:
    - expr (str): A string representing a mathematical expression.

    Returns:
    - f (function): The function represented by the expression.
    """

    f_str = expr

    eval_context = {"x": None}
    eval_context.update(math.__dict__)

    def f(x):
        eval_context["x"] = x
        return eval(f_str, eval_context)

    return f
