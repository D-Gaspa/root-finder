def false_position(f, a, b, tol=1e-5, max_iter=100):
    """False Position method for finding a root of a function.

    Parameters:
    - f (function): Function to find the root of.
    - a, b (float): The interval [a, b] within which to search for the root.
    - tol (float): The tolerance level for stopping the algorithm.
    - max_iter (int): Maximum number of iterations.

    Returns:
    - x (float): The root of the function.
    - n (int): The number of iterations required to reach the root.

    Raises:
    - ValueError: If the root is not in the interval [a, b], or the maximum number of iterations is exceeded.
    """

    # Compute the function values
    f_a = f(a)
    f_b = f(b)

    # Check if the root is in the interval [a, b]
    if f_a * f_b > 0:
        raise ValueError("Root not in interval [a, b].")

    # Initialize variables
    n = 0
    x = a - (f_a * (b - a)) / (f_b - f_a)

    # Loop until the root is found or the maximum number of iterations is reached
    while abs(f(x)) > tol and n < max_iter:
        f_x = f(x)

        # Check if the root is in the interval [a, x] or [x, b]
        if f_a * f_x < 0:
            b, f_b = x, f_x
        else:
            a, f_a = x, f_x

        # Update x using the False Position formula
        x = a - (f_a * (b - a)) / (f_b - f_a)
        n += 1

    # Check for convergence
    if n == max_iter:
        raise ValueError("Exceeded maximum iterations. Adjust the initial interval, tolerance, or try another method.")

    return x, n
