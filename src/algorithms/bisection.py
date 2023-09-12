def bisection(f, a, b, tol=1e-5, max_iter=100):
    """Bisection method for finding a root of a function.

    Parameters:
    - f (function): Function to find the root of.
    - a, b (float): The interval [a, b] within which to search for the root.
    - tol (float): The tolerance level for stopping the algorithm.
    - max_iter (int): Maximum number of iterations.

    Returns:
    - x (float): The root of the function.
    - n (int): The number of iterations required to reach the root.

    Raises: - ValueError: If the function does not change sign within the interval [a, b] or the maximum number of
    iterations is exceeded.
    """

    # Check if the function changes sign within the interval [a, b]
    if f(a) * f(b) > 0:
        raise ValueError("The function does not change sign within the interval [a, b].")

    # Initialize variables
    n = 0

    # Loop until the root is found or the maximum number of iterations is reached
    while abs(b - a) > tol and n < max_iter:
        x = (a + b) / 2

        # Check if the function value at the root approximation is sufficiently close to zero
        if abs(f(x)) <= tol:
            return x, n

        # Check if the root is in the interval [a, x] or [x, b]
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

        # Update iteration count
        n += 1

    # Check for convergence
    if n == max_iter:
        raise ValueError("Exceeded maximum iterations. Adjust the initial interval, tolerance, or try another method.")

    return (a + b) / 2, n
