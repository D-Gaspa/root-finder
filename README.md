# Root-Finder

`Root-Finder` is a Python application built using PyQt5 for finding the roots of mathematical functions using various methods, such as Bisection, False Position, Newton's, Modified Newton's, and Secant methods. It offers a user-friendly GUI, allowing users to visualize functions and results easily.

<div style="display: flex; justify-content: center;">
    <img src="assets/Root-finder1.png" width="410" style="margin-right: 20px;" alt="Main interface">
    <img src="assets/Root-finder2.png" width="410" alt="Main interface (Dark Mode)">
</div>

## Features

- **Function Visualization**: Plot any function and view its curve on a graph.
- **LaTeX Support**: Input your mathematical expression and view it in beautifully formatted LaTeX.
- **Multiple Methods**: Choose from several methods to compute the roots.
- **Dark Mode**: Toggle between light and dark themes to match your mood and preferences.
- **Intuitive UI**: Easily insert mathematical symbols with a single click.

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/D-Gaspa/root-finder.git
```

2. Navigate to the project directory and install required packages:
```bash
cd Root-Finder
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. Enter your function in the provided input box.
2. Choose a root-finding method from the dropdown menu.
3. Provide the required parameters for the selected method.
4. Click on `Calculate` to compute the root.
5. View the results in the results display and the graph.

## Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Methods

### Bisection Method

The Bisection method is one of the simplest and most reliable methods for solving equations of the form $f(x) = 0$. It's based on the Intermediate Value Theorem which states that if a continuous function $f$ defined over an interval $[a, b]$ takes on opposite signs at the end points $a$ and $b$, i.e., $f(a) \times f(b) < 0$, then there exists at least one root $c$ in the interval $(a, b)$.

#### Steps of the Bisection Method:
1. **Initial Interval**: Start with an interval $[a, b]$ where the function $f$ changes sign. This can be verified by checking $f(a) \times f(b) < 0$.
2. **Calculate Midpoint**: Compute the midpoint of the interval: $x = \frac{a+b}{2}$.
3. **Function Evaluation**: Evaluate $f(x)$.
4. **Update Interval**: If $f(a) \times f(x) < 0$, it means the root lies in the interval $[a, x]$. Otherwise, the root lies in the interval $[x, b]$. Update the interval accordingly.
5. **Convergence Check**: If the width of the interval $|b-a|$ is smaller than a given tolerance or if the absolute value of $f(x)$ is less than the tolerance, then stop. Otherwise, return to Step 2.
6. **Iteration Limit**: If the number of iterations exceeds a specified maximum, the method may terminate with an error message.

#### Corresponding Code:
1. The initial check for sign change:
```python
if f(a) * f(b) > 0:
   raise ValueError("The function does not change sign within the interval [a, b].")
```
2. The midpoint calculation:
```python
x = (a + b) / 2
```
3. Evaluating the function at $ x $:
```python
if abs(f(x)) <= tol:
   return x, n
```
4. Updating the interval:
```python
if f(a) * f(x) < 0:
   b = x
else:
   a = x
```
5. Convergence checks are present in the loop condition:
```python
while abs(b - a) > tol and n < max_iter:
```
6. Iteration limit check:
```python
if n == max_iter:
   raise ValueError("Exceeded maximum iterations. Adjust the initial interval, tolerance, or try another method.")
```
   
### False Position Method (Regula Falsi)

The False Position method, also known as the Regula Falsi method, is a bracketing method like the Bisection method. The primary difference is how the root approximation is obtained. Instead of simply taking the midpoint of the interval, the False Position method linearly interpolates between the two current estimates and chooses the x-intercept of the resulting line as the next approximation. It's worth noting that while the method always converges, it might not always converge to the closest root.

#### Steps of the False Position Method:

1. **Initial Interval**: Start with an interval $[a, b]$ where the function $f$ changes sign. This can be verified by checking $f(a) \times f(b) < 0$.
2. **Calculate Root Approximation**: Use the formula:

    $$x = a - \frac{f(a) \times (b - a)}{f(b) - f(a)}$$

    to compute the next approximation for the root.
3. **Function Evaluation**: Evaluate $f(x)$.
4. **Update Interval**: If $f(a) \times f(x) < 0$, it means the root lies in the interval $[a, x]$. Otherwise, the root lies in the interval $[x, b]$. Update the interval accordingly.
5. **Convergence Check**: If the absolute value of $f(x)$ is less than the tolerance, then stop. Otherwise, return to Step 2.
6. **Iteration Limit**: If the number of iterations exceeds a specified maximum, the method may terminate with an error message.

#### Corresponding Code:
1. The initial check for sign change:
```python
if f_a * f_b > 0:
   raise ValueError("Root not in interval [a, b].")
```
2. The root approximation calculation:
```python
x = a - (f_a * (b - a)) / (f_b - f_a)
```
3. Evaluating the function at $x$:
```python
f_x = f(x)
```
4. Updating the interval:
```python
if f_a * f_x < 0:
   b, f_b = x, f_x
else:
   a, f_a = x, f_x
```
5. Convergence checks are present in the loop condition:
```python
while abs(f(x)) > tol and n < max_iter:
```
6. Iteration limit check:
```python
if n == max_iter:
   raise ValueError("Exceeded maximum iterations. Adjust the initial interval, tolerance, or try another method.")
```

### Newton's Method (Newton-Raphson)

Newton's method, often referred to as the Newton-Raphson method, is an iterative numerical method used to find successively better approximations to the roots of a real-valued function. It uses information about the function's derivative to improve the approximation. The method starts with an initial guess and refines this guess using the function's value and its derivative. The convergence rate of the Newton-Raphson method is quadratic, provided the initial guess is close enough to the true root and the function satisfies certain conditions. However, if the initial guess is not close, the method can diverge.

#### Steps of the Newton-Raphson Method:

1. **Initial Guess**: Start with an initial guess $x_0$ for the root.
2. **Check Derivative**: Ensure that the derivative $f'(x_0)$ is not zero. If it's zero, the method cannot proceed as it would lead to a division by zero.
3. **Update Formula**: Use the formula:

   $$x_{\text{new}} = x_{\text{old}} - \frac{f(x_{\text{old}})}{f'(x_{\text{old}})}$$

   to compute the next approximation for the root.
4. **Function Evaluation**: Evaluate $f(x_{\text{new}})$.
5. **Convergence Check**: If the absolute value of $f(x_{\text{new}})$ is less than the tolerance, then stop. Otherwise, update $x_{\text{old}}$ with $x_{\text{new}}$ and return to Step 3.
6. **Iteration Limit**: If the number of iterations exceeds a specified maximum, the method may terminate with an error message.

#### Corresponding Code:
1. Initial check for zero derivative:
```python
if df(x0) == 0:
   raise ValueError("Derivative is zero at the initial guess.")
```
2. Setting the initial guess:
```python
x = x0
```
3. The Newton update formula:
```python
x = x - f(x) / df(x)
```
4. Evaluating the function at the new guess:
(This is implicit in the update formula and the loop condition.)
5. Convergence checks are present in the loop condition:
```python
while abs(f(x)) > tol and n < max_iter:
```
6. Iteration limit check:
```python
if n == max_iter:
 raise ValueError("Exceeded maximum iterations. Adjust the initial guess, tolerance, or try another method.")
```

### Modified Newton's Method

The Modified Newton's method is a variant of the classic Newton-Raphson method, designed to improve convergence in cases where the traditional method might be slow or fail to converge. The modification involves using both the first and second derivatives of the function. This method can be particularly useful when $f'(x)$ is close to zero, which can cause the standard Newton-Raphson method to take large steps.

#### Steps of the Modified Newton's Method:

1. **Initial Guess**: Start with an initial guess $x_0$ for the root.
2. **Compute Derivatives**: Calculate the first $f'(x)$ and second $f''(x)$ derivatives of the function at the current approximation.
3. **Update Formula**: Use the modified formula:

   $$x_{\text{new}} = x_{\text{old}} - \frac{f(x_{\text{old}}) \times f'(x_{\text{old}})}{f'(x_{\text{old}})^2 - f(x_{\text{old}}) \times f''(x_{\text{old}})}$$
   
   to compute the next approximation for the root.
4. **Convergence Check**: If the absolute value of $f(x_{\text{new}})$ is less than the tolerance, then stop. Otherwise, return to Step 2.
5. **Denominator Check**: If the denominator $f'(x_{\text{old}})^2 - f(x_{\text{old}}) \times f''(x_{\text{old}})$ becomes zero, the method might fail to provide a valid update and should be stopped.
6. **Iteration Limit**: If the number of iterations exceeds a specified maximum, the method may terminate with an error message.

#### Corresponding Code:
1. Initial guess assignment:
```python
x = x0
```
2. Calculation of derivatives:
```python
fx = f(x)
dfx = df(x)
ddfx = ddf(x)
```
3. The modified Newton update formula:
```python
x = x - (fx * dfx) / (dfx**2 - fx * ddfx)
```
4. Convergence check:
```python
if abs(fx) < tol:
   return x, n
```
5. Denominator check:
```python
denominator = dfx**2 - fx * ddfx
if denominator == 0:
   raise ValueError("Denominator became zero. Adjust the initial guess or use another method.")
```
6. Iteration limit check:
```python
raise ValueError("Exceeded maximum iterations. Adjust the initial guess, tolerance, or try another method.")
```

### Secant Method

The Secant method is an iterative root-finding method that uses linear interpolation based on two initial approximations to the root. It's an open method, meaning it doesn't require the function to change sign over an interval (as in the Bisection method). The secant method typically converges more slowly than the Newton-Raphson method, but it converges faster than the bisection method. Its convergence rate is superlinear but not quadratic like Newton's method.

#### Steps of the Secant Method:
1. **Initial Guesses**: Start with two initial approximations $x_0$ and $x_1$ for the root.
2. **Secant Formula**: Use the formula:

   $$x_{\text{new}} = x_1 - f(x_1) \times \frac{x_1 - x_0}{f(x_1) - f(x_0)}$$

   to compute the next approximation for the root.
3. **Update Approximations**: For the next iteration, use the most recent two approximations $x_1$ and $x_{\text{new}}$.
4. **Convergence Check**: If the absolute difference between two consecutive approximations $|x_{\text{new}} - x_1|$ is less than the tolerance, then stop. Otherwise, return to Step 2.
5. **Denominator Check**: If the difference in function values $f(x_1) - f(x_0)$ approaches zero, this will result in division by zero in the formula. The method should be stopped in this case.
6. **Iteration Limit**: If the number of iterations exceeds a specified maximum, the method may terminate with an error message.

#### Corresponding Code:
1. Initial guesses assignment:
```python
x = x1
```
2. The secant method formula:
```python
x = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
```
3. Updating the approximations:
```python
x0, x1 = x1, x
```
4. Convergence check:
```python
while abs(x1 - x0) > tol and n < max_iter:
```
5. Denominator check:
```python
if f_x1 - f_x0 == 0:
    raise ValueError("Denominator approaching zero. Try different initial values or another method.")
```
6. Iteration limit check:
```python
if n == max_iter:
  raise ValueError("Exceeded maximum iterations. Adjust the initial guesses, tolerance, or try another method.")
```
---

### General Notes:

- For all methods, the choice of initial guess(es) is crucial. A poor choice can lead to slow convergence or even divergence in some methods.
- Most methods in this guide have been implemented with error checks to handle edge cases and prevent the methods from failing in unexpected ways. For example, checks against zero denominators are crucial to avoid division by zero errors.
- Consistent formatting and clear explanations enhance the readability and understanding of the methods and their implementations.