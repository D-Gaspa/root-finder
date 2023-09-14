def secant(f, x0, x1, tol=1e-5, max_iter=100):
    """Secant method for finding a root of a function.

    Parameters:
    - f (function): Function to find the root of.
    - x0, x1 (float): Two initial guesses for the root.
    - tol (float): The tolerance level for stopping the algorithm.
    - max_iter (int): Maximum number of iterations.

    Returns:
    - x (float): The root of the function.
    - n (int): The number of iterations required to reach the root.

    Raises:
    - ValueError: If a suitable root isn't found within max_iter iterations.
    """

    # Explicit check for identical function values at initial guesses
    if f(x0) == f(x1):
        raise ValueError("Function values of the two guesses are the same, causing division by zero.")

    # Initialize variables
    n = 0
    x = x1

    while abs(x1 - x0) > tol and n < max_iter:
        # Compute the function values
        f_x0 = f(x0)
        f_x1 = f(x1)

        # Avoid division by zero
        if f_x1 - f_x0 == 0:
            raise ValueError("Denominator approaching zero. Try different initial values or another method.")

        # Secant method formula
        x = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Prepare for the next iteration
        x0, x1 = x1, x
        n += 1

    # Check for convergence
    if n == max_iter:
        raise ValueError("Exceeded maximum iterations. Adjust the initial guesses, tolerance, or try another method.")

    return x, n
