def newton(f, df, x0, tol=1e-5, max_iter=100):
    """Newton method for finding a root of a function.

    Parameters:
    - f (function): Function to find the root of.
    - df (function): Derivative of the function.
    - x0 (float): Initial guess for the root.
    - tol (float): The tolerance level for stopping the algorithm.
    - max_iter (int): Maximum number of iterations.

    Returns:
    - x (float): The root of the function.
    - n (int): The number of iterations required to reach the root.

    Raises:
    - ValueError: If the derivative is zero at the initial guess or the maximum number of iterations is exceeded.
    """

    # Check if the derivative is zero at the initial guess
    if df(x0) == 0:
        raise ValueError("Derivative is zero at the initial guess.")

    # Initialize variables
    x = x0
    n = 0

    # Loop until the root is found or the maximum number of iterations is reached
    while abs(f(x)) > tol and n < max_iter:
        # Update x using the Newton formula
        x = x - f(x) / df(x)

        # Update iteration count
        n += 1

    # Check for convergence
    if n == max_iter:
        raise ValueError("Exceeded maximum iterations. Adjust the initial guess, tolerance, or try another method.")

    return x, n
