def modified_newton(f, df, ddf, x0, tol=1e-5, max_iter=100):
    """Modified Newton method for finding a root of a function.

    Parameters:
    - f (function): Function to find the root of.
    - df (function): First derivative of the function.
    - ddf (function): Second derivative of the function.
    - x0 (float): Initial guess for the root.
    - tol (float): The tolerance level for stopping the algorithm.
    - max_iter (int): Maximum number of iterations.

    Returns:
    - x (float): The root of the function.
    - n (int): The number of iterations required to reach the root.

    Raises:
    - ValueError: If the denominator becomes zero or the maximum number of iterations is exceeded.
    """

    # Initialize variables
    x = x0

    # Loop until the root is found or the maximum number of iterations is reached
    for n in range(max_iter):
        # Compute the function values
        fx = f(x)
        dfx = df(x)
        ddfx = ddf(x)

        # Check for convergence
        if abs(fx) < tol:
            return x, n

        # Check for zero in the denominator
        denominator = dfx ** 2 - fx * ddfx
        if denominator == 0:
            raise ValueError("Denominator became zero. Adjust the initial guess or use another method.")

        # Update x using the Modified Newton formula
        x = x - (fx * dfx) / denominator

    # Check for convergence
    raise ValueError("Exceeded maximum iterations. Adjust the initial guess, tolerance, or try another method.")
