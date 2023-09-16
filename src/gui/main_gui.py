import io
import re
import sys
import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from src.algorithms.bisection import bisection
from src.algorithms.false_position import false_position
from src.algorithms.modified_newton import modified_newton
from src.algorithms.newton import newton
from src.algorithms.secant import secant
from src.utils.function_evaluation import get_function_and_derivatives
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def preprocess_input(expression):
    """
    Preprocess the expression to handle implicit multiplications and exponentiation.
    e.g. "2x" becomes "2*x" and "x^2" becomes "x**2".
    """
    # Use a regex to find all instances of a number followed by a letter (e.g., "2x")
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

    # Replace ^ with ** for exponentiation
    expression = expression.replace('^', '**')

    return expression


def convert_to_latex(expression):
    """
    Convert a plain text mathematical expression to LaTeX format using SymPy.
    Returns a tuple containing the LaTeX expression and the Python-friendly expression.
    """
    # Preprocess the expression to handle implicit multiplications
    python_expr = preprocess_input(expression)

    # Convert to SymPy expression
    expr = sp.sympify(python_expr)

    # Convert to LaTeX
    latex_expr = sp.latex(expr, mul_symbol='dot')

    # Post-process: Remove any unwanted 'cdot' to handle implicit multiplications
    latex_expr = latex_expr.replace('\\cdot', '')

    return latex_expr, python_expr


def get_dark_palette():
    """
    Returns the dark palette.
    """
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(68, 68, 68))  # Darker button color
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    return dark_palette


def get_dark_stylesheet():
    """
    Returns the dark mode stylesheet.
    """
    return """
    QWidget {
        background-color: #333;
        color: white;
    }
    QToolTip { 
        color: #ffffff; 
        background-color: #2a82da; 
        border: 1px solid white; 
    }
    QComboBox, QLineEdit {
        background-color: #333;
        border: 1px solid #555;
    }
    QComboBox::hover, QLineEdit::hover, QToolButton::hover {
        background-color: #444;
    }
    QPushButton {
        background-color: #444;
        border: 1px solid #555;  # Restore border for the button
    }
    QPushButton:hover {
        background-color: #555;
    }
    QToolBar QToolBar QToolButton:pressed, QToolBar QToolButton:checked, QToolBar QToolButton {
        background-color: #333;
    }
    QToolBar {  # This targets all toolbars
        border: none;  # Remove border from all toolbars
        background-color: #333;  # Ensure toolbar background matches
    }
    QToolBar::hover {  # Explicitly set the hover color for QToolBar
        background-color: #333;
    }
    """


def toggle_dark_mode():
    """
    Toggle between dark mode and light mode.
    """
    # Define a dark palette
    dark_palette = get_dark_palette()

    # Toggle between the default palette and dark palette
    if app.palette() != dark_palette:
        app.setPalette(dark_palette)
        app.setStyleSheet(get_dark_stylesheet())
    else:
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("")

    # Update the LaTeX display
    window.update_latex_display()

    # Update the results display
    window.on_calculate_clicked()

    # Update the graph display
    window.graph_display.refresh_style()


def is_float(value, allow_empty=False):
    """Check if a value is a float or optionally empty."""
    try:
        float(value)
        return True
    except ValueError:
        return allow_empty and value == ""


def is_int(value, allow_empty=False):
    """Check if a value is an integer or optionally empty."""
    try:
        int(value)
        return True
    except ValueError:
        return allow_empty and value == ""


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.parent = parent
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super(GraphCanvas, self).__init__(fig)

        self.toolbar = self.get_toolbar()
        if self.toolbar:
            configure_subplots_action = next(
                (action for action in self.toolbar.actions() if action.text() == "Customize"), None)
            if configure_subplots_action:
                self.toolbar.removeAction(configure_subplots_action)

        # Set initial colors
        self.set_colors_based_on_theme()

    def get_toolbar(self):
        """Get the navigation toolbar."""
        for widget in self.parent.findChildren(QWidget):
            if isinstance(widget, NavigationToolbar):
                # Remove the "Configure subplots" button
                for action in widget.actions():
                    if action.iconText() == 'Subplots':
                        widget.removeAction(action)
                return widget
        return None

    def set_colors_based_on_theme(self):
        """Adjust graph colors based on the application's theme."""
        if app.palette().color(QPalette.Window) == QColor(53, 53, 53):  # Dark mode
            self.figure.set_facecolor('black')
            self.axes.set_facecolor('black')
            self.axes.grid(color='gray')
            self.axes.spines['bottom'].set_color('gray')
            self.axes.spines['top'].set_color('gray')
            self.axes.spines['left'].set_color('gray')
            self.axes.spines['right'].set_color('gray')
            self.axes.tick_params(axis='x', colors='gray')
            self.axes.tick_params(axis='y', colors='gray')
            self.axes.yaxis.label.set_color('gray')
            self.axes.xaxis.label.set_color('gray')
            self.axes.axhline(0, color='white', linewidth=1)  # Horizontal line (y-axis)
            self.axes.axvline(0, color='white', linewidth=1)  # Vertical line (x-axis)

        else:  # Light mode
            self.figure.set_facecolor('white')
            self.axes.set_facecolor('white')
            self.axes.grid(color='lightgray')
            self.axes.spines['bottom'].set_color('black')
            self.axes.spines['top'].set_color('black')
            self.axes.spines['left'].set_color('black')
            self.axes.spines['right'].set_color('black')
            self.axes.tick_params(axis='x', colors='black')
            self.axes.tick_params(axis='y', colors='black')
            self.axes.yaxis.label.set_color('black')
            self.axes.xaxis.label.set_color('black')
            self.setStyleSheet("")
            self.axes.axhline(0, color='black', linewidth=1)  # Horizontal line (y-axis)
            self.axes.axvline(0, color='black', linewidth=1)  # Vertical line (x-axis)

    def refresh_style(self):
        """Refresh the graph's appearance based on the application theme."""
        self.set_colors_based_on_theme()
        self.draw()

    def clear_graph(self):
        """Clear the graph and reset the appearance."""
        self.axes.clear()
        self.set_colors_based_on_theme()
        self.draw()


class RootFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window properties
        self.setWindowTitle("Root Finder")
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QVBoxLayout()

        # Dark Mode Icon (placeholder)
        self.right_toolbar = QToolBar()
        spacer = QWidget()  # Spacer to push the icon to the right
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_toolbar.addWidget(spacer)
        self.right_toolbar.addAction(QIcon(), "Toggle Dark Mode", toggle_dark_mode)
        self.right_toolbar.setMovable(False)  # Ensure the toolbar stays in place
        main_layout.addWidget(self.right_toolbar)

        # Math Symbols Toolbar
        self.math_symbols_toolbar = QToolBar()
        # Dictionary mapping symbols to insertion behaviors
        symbols = {
            "x": "x",
            "x^2": "x^2",
            "x^3": "x^3",
            "x^n": "x^",
            "^": "^",
            "sqrt()": "sqrt(|)",
            "sin()": "sin(|)",
            "cos()": "cos(|)",
            "tan()": "tan(|)",
            "log()": "log(|)",
            "e": "e",
            "pi": "pi",
            "(": "(",
            ")": ")"
        }
        for symbol, insert_behavior in symbols.items():
            action = self.math_symbols_toolbar.addAction(symbol)
            action.triggered.connect(lambda _, s=insert_behavior: self.insert_symbol(s))
        main_layout.addWidget(self.math_symbols_toolbar)

        # Input & Method Widgets
        input_layout = QHBoxLayout()
        self.fx_input = QLineEdit()
        self.fx_input.setPlaceholderText("Enter f(x) here...")
        self.fx_input.textChanged.connect(self.update_latex_display)
        self.fx_input.textChanged.connect(self.validate_input)
        method_label = QLabel("Methods:")
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["Bisection", "False Position", "Modified Newton", "Newton", "Secant"])
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.on_calculate_clicked)

        input_layout.addWidget(self.fx_input)
        input_layout.addWidget(method_label)
        input_layout.addWidget(self.method_dropdown)
        input_layout.addWidget(self.calculate_button)
        main_layout.addLayout(input_layout)

        self.method_dropdown.setCurrentIndex(-1)  # Set no method selected

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("background-color: red; color: white; border: none;")
        clear_button.clicked.connect(self.clear_inputs)
        main_layout.addWidget(clear_button)

        # LaTeX Display Area
        self.latex_display_label = QLabel("Your f(x):")
        self.latex_display_image_label = QLabel()  # This will hold the rendered image
        self.error_display_label = QLabel()  # This will display error messages

        # Set the font size for the error label
        font = self.error_display_label.font()
        font.setPointSize(10)  # Adjust this value as needed
        self.error_display_label.setFont(font)

        main_layout.addWidget(self.latex_display_label)
        main_layout.addWidget(self.latex_display_image_label)
        main_layout.addWidget(self.error_display_label)

        # Additional Parameters Area
        self.additional_params_layout = QVBoxLayout()
        self.param_widgets = {}  # Store the parameter widgets for easy access
        main_layout.addLayout(self.additional_params_layout)

        # Results Display (placeholder for now)
        self.results_display = QTextEdit()
        self.results_display.setPlaceholderText("Results will be displayed here...")
        main_layout.addWidget(self.results_display)

        # Connect method dropdown change to adjust additional parameters
        self.method_dropdown.currentTextChanged.connect(self.adjust_parameters)

        # Graph Visualization
        self.graph_display = GraphCanvas(self, width=5, height=4, dpi=100)
        self.graph_toolbar = NavigationToolbar(self.graph_display, self)
        main_layout.addWidget(self.graph_toolbar)  # Add the toolbar to the main layout
        # Set the toolbar's background color of the icons to red
        self.graph_toolbar.setStyleSheet("""
                QToolButton {
                    background-color: red;
                    border: none;
                }
                QToolButton:hover {
                    background-color: white;
                }
            """)

        # Using QSplitter to allow resizing sections
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(main_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.graph_display)

        self.setCentralWidget(splitter)

        self.validate_input()

    def clear_inputs(self):
        """Clear all inputs and reset styles."""
        self.fx_input.clear()
        for widget in self.param_widgets.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
                widget.setStyleSheet("")
        # Clear the graph
        self.graph_display.clear_graph()

    def reset_results(self):
        """Clear the results display."""
        self.results_display.clear()

    def validate_input(self):
        """
        Validates all input fields.
        Returns True if all inputs are valid, else False.
        """
        valid = True

        # Clear previous invalid input borders
        for widget in self.param_widgets.values():
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet("")

        # 1. f(x) validation
        if not self.fx_input.text().strip() or self.error_display_label.text():
            valid = False

        # 2. Method selection validation
        if self.method_dropdown.currentIndex() == -1:
            valid = False

        # 3. Additional parameter validation
        method = self.method_dropdown.currentText()

        # a, b validation for Bisection and False Position
        if method in ["Bisection", "False Position"]:
            a_val, b_val = self.param_widgets['a'].text(), self.param_widgets['b'].text()

            # Reset styles first
            self.param_widgets['a'].setStyleSheet("")
            self.param_widgets['b'].setStyleSheet("")

            if not is_float(a_val) or not a_val:
                self.param_widgets['a'].setStyleSheet("border: 2px solid red;")
                valid = False

            if not is_float(b_val) or not b_val or (
                    is_float(a_val) and is_float(b_val) and float(b_val) <= float(a_val)):
                self.param_widgets['b'].setStyleSheet("border: 2px solid red;")
                valid = False

        # x0 validation for Newton and Modified Newton
        if method in ["Newton", "Modified Newton"]:
            x0_val = self.param_widgets['x0'].text()

            # Reset style first
            self.param_widgets['x0'].setStyleSheet("")

            if not is_float(x0_val) or not x0_val:
                self.param_widgets['x0'].setStyleSheet("border: 2px solid red;")
                valid = False

        # x0, x1 validation for Secant
        if method == "Secant":
            x0_val, x1_val = self.param_widgets['x0'].text(), self.param_widgets['x1'].text()

            # Reset styles first
            self.param_widgets['x0'].setStyleSheet("")
            self.param_widgets['x1'].setStyleSheet("")

            if not is_float(x0_val) or not x0_val:
                self.param_widgets['x0'].setStyleSheet("border: 2px solid red;")
                valid = False

            if not is_float(x1_val) or not x1_val:
                self.param_widgets['x1'].setStyleSheet("border: 2px solid red;")
                valid = False

        # tol validation (if provided)
        if self.param_widgets.get('tol'):
            tol_text = self.param_widgets['tol'].text().strip()
            if tol_text and not is_float(tol_text):
                self.param_widgets['tol'].setStyleSheet("border: 2px solid red;")
                valid = False

        # max_iter validation (if provided)
        if self.param_widgets.get('max_iter'):
            max_iter_text = self.param_widgets['max_iter'].text().strip()
            if max_iter_text and not is_int(max_iter_text):
                self.param_widgets['max_iter'].setStyleSheet("border: 2px solid red;")
                valid = False

        # 4. Update the button color based on validation
        if valid:
            self.calculate_button.setStyleSheet("background-color: #4CAF50;")  # Green color
        else:
            self.calculate_button.setStyleSheet("background-color: #444;")  # Default color

        return valid

    def adjust_parameters(self):
        """
        Adjust additional parameter input fields based on the selected method.
        """
        method = self.method_dropdown.currentText()

        # Store the current values
        current_values = {}
        for key, widget in self.param_widgets.items():
            if isinstance(widget, QLineEdit):
                current_values[key] = widget.text()

        # Clear previous widgets
        for widget in self.param_widgets.values():
            if isinstance(widget, QLineEdit):
                widget.textChanged.disconnect(self.validate_input)
            widget.deleteLater()
        self.param_widgets.clear()

        # Return if no method is selected
        if method == "":
            return

        # Depending on the method, create the required input fields
        if method in ["Bisection", "False Position"]:
            self.param_widgets['a_label'] = QLabel("a:")
            self.param_widgets['a'] = QLineEdit(self)
            self.param_widgets['a'].setPlaceholderText("Enter a here...")
            self.param_widgets['a'].setText(current_values.get('a', ''))  # Restore value if it exists

            self.param_widgets['b_label'] = QLabel("b:")
            self.param_widgets['b'] = QLineEdit(self)
            self.param_widgets['b'].setPlaceholderText("Enter b here...")
            self.param_widgets['b'].setText(current_values.get('b', ''))  # Restore value if it exists

            self.additional_params_layout.addWidget(self.param_widgets['a_label'])
            self.additional_params_layout.addWidget(self.param_widgets['a'])
            self.additional_params_layout.addWidget(self.param_widgets['b_label'])
            self.additional_params_layout.addWidget(self.param_widgets['b'])

        elif method in ["Modified Newton", "Newton"]:
            self.param_widgets['x0_label'] = QLabel("x0 (Initial Guess):")
            self.param_widgets['x0'] = QLineEdit(self)
            self.param_widgets['x0'].setPlaceholderText("Enter x0 here...")
            self.param_widgets['x0'].setText(current_values.get('x0', ''))  # Restore value if it exists

            self.additional_params_layout.addWidget(self.param_widgets['x0_label'])
            self.additional_params_layout.addWidget(self.param_widgets['x0'])

        elif method == "Secant":
            self.param_widgets['x0_label'] = QLabel("x0 (First Initial Guess):")
            self.param_widgets['x0'] = QLineEdit(self)
            self.param_widgets['x0'].setPlaceholderText("Enter x0 here...")

            self.param_widgets['x1_label'] = QLabel("x1 (Second Initial Guess):")
            self.param_widgets['x1'] = QLineEdit(self)
            self.param_widgets['x1'].setPlaceholderText("Enter x1 here...")

            self.additional_params_layout.addWidget(self.param_widgets['x0_label'])
            self.additional_params_layout.addWidget(self.param_widgets['x0'])
            self.additional_params_layout.addWidget(self.param_widgets['x1_label'])
            self.additional_params_layout.addWidget(self.param_widgets['x1'])

        # Add optional tolerance and max iterations for all methods
        self.param_widgets['tol_label'] = QLabel("Tolerance:")
        self.param_widgets['tol'] = QLineEdit(self)
        self.param_widgets['tol'].setPlaceholderText("Default: 1e-5")

        self.param_widgets['max_iter_label'] = QLabel("Max Iterations:")
        self.param_widgets['max_iter'] = QLineEdit(self)
        self.param_widgets['max_iter'].setPlaceholderText("Default: 100")

        self.additional_params_layout.addWidget(self.param_widgets['tol_label'])
        self.additional_params_layout.addWidget(self.param_widgets['tol'])
        self.additional_params_layout.addWidget(self.param_widgets['max_iter_label'])
        self.additional_params_layout.addWidget(self.param_widgets['max_iter'])

        # Connect all textChanged signals to validate_input and reset_results
        for widget in self.param_widgets.values():
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(self.validate_input)
                widget.textChanged.connect(self.reset_results)  # Reset results when any parameter changes

        self.validate_input()  # Validate the input fields

    def insert_symbol(self, symbol):
        # Set focus to fx_input
        self.fx_input.setFocus()

        cursor_position = self.fx_input.cursorPosition()
        current_text = self.fx_input.text()

        # If the symbol has a |, it indicates where the cursor should be placed after insertion
        cursor_offset = symbol.count('|')
        symbol = symbol.replace('|', '')

        new_text = current_text[:cursor_position] + symbol + current_text[cursor_position:]
        self.fx_input.setText(new_text)
        self.fx_input.setCursorPosition(cursor_position + len(symbol) - cursor_offset)

    def plot_function_graph(self, python_expr, latex_expr):
        """
        Plots the graph of the function given its python expression and latex expression.
        """
        try:
            x_center = 0
            x_vals = np.linspace(x_center - 10, x_center + 10, 400)
            y_vals = []
            for val in x_vals:
                try:
                    y = eval(python_expr, {
                        "x": val,
                        "sqrt": math.sqrt,
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan,
                        "log": math.log,
                        "pi": math.pi,
                        "e": math.e
                    })
                    y_vals.append(y)
                except ValueError:
                    y_vals.append(float('nan'))

            # Clear previous plots
            self.graph_display.axes.clear()

            # Adjust graph background and grid based on dark mode
            self.graph_display.set_colors_based_on_theme()

            # Plot the function
            self.graph_display.axes.plot(x_vals, y_vals, 'r-', label=f"${latex_expr}$", linewidth=2, zorder=1)

            # Set labels and legend
            self.graph_display.axes.set_xlabel('x')
            self.graph_display.axes.set_ylabel('f(x)')
            self.graph_display.axes.legend()

            # Draw the updated graph
            self.graph_display.draw()

        except Exception as e:
            self.graph_display.setText(f"Error while plotting: {str(e)}")

    def update_latex_display(self):
        """
        Update the LaTeX display label with the current input.
        """
        # Get the current input
        expression = self.fx_input.text()

        # Clear previous display
        self.latex_display_image_label.clear()

        # Check if input area is empty
        if not expression.strip():
            self.latex_display_image_label.clear()
            self.error_display_label.clear()
            self.fx_input.setStyleSheet("")  # Reset input border
            return

        # Convert to LaTeX
        try:
            latex_expr, python_expr = convert_to_latex(expression)
        except Exception as e:
            self.error_display_label.setText(f"Error in conversion:\n{str(e)}")
            self.latex_display_image_label.clear()
            self.fx_input.setStyleSheet("border: 2px solid red;")  # Set input border to red
            return

        # Render LaTeX using matplotlib and set to QLabel
        try:
            fig, ax = plt.subplots(figsize=(5, 1))
            text_color = 'white' if app.palette().color(QPalette.Window) == QColor(53, 53, 53) else 'black'
            ax.text(0.5, 0.5, f'${latex_expr}$', size=20, va='center', ha='center', color=text_color)
            ax.axis('off')
            fig.patch.set_facecolor(self.palette().window().color().name())  # Set background color
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
            plt.close(fig)
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())
            self.latex_display_image_label.setPixmap(pixmap)
            self.error_display_label.clear()
            self.fx_input.setStyleSheet("")  # Reset input border

            # Plot the graph
            self.plot_function_graph(python_expr, latex_expr)

        except Exception as e:
            # If there's any error in rendering, display an error message directly without any LaTeX wrapping
            self.error_display_label.setText(f"Your current input is invalid:\n{str(e)}")
            self.fx_input.setStyleSheet("border: 2px solid red;")  # Set input border to red

    def on_calculate_clicked(self):
        """
        Calculate the root using the selected method.
        """
        # If the inputs aren't valid, just return without doing anything
        if not self.validate_input():
            return

        # Clear previous results and graph
        self.graph_display.clear_graph()
        self.results_display.clear()

        # Capture the user's function
        latex_expr, python_expr = convert_to_latex(self.fx_input.text())

        # Placeholder for results
        root = None
        iterations = None
        error_msg = None

        # Parameters to plot
        plot_points = []

        # Check the method selected
        method = self.method_dropdown.currentText()

        # Get the functions and derivatives
        f, df, ddf = get_function_and_derivatives(python_expr)

        if method == "Bisection" or method == "False Position":
            a = float(self.param_widgets['a'].text())
            b = float(self.param_widgets['b'].text())
            tol = float(self.param_widgets['tol'].text() or "1e-5")
            max_iter = int(self.param_widgets['max_iter'].text() or "100")

            plot_points.extend([a, b])

            if method == "Bisection":
                try:
                    # Execute the bisection method
                    root, iterations = bisection(f, a, b, tol, max_iter)
                except ValueError as e:
                    error_msg = str(e)
            else:
                try:
                    # Execute the false position method
                    root, iterations = false_position(f, a, b, tol, max_iter)
                except ValueError as e:
                    error_msg = str(e)

        elif method == "Newton" or method == "Modified Newton":
            x0 = float(self.param_widgets['x0'].text())
            plot_points.append(x0)
            tol = float(self.param_widgets['tol'].text() or "1e-5")
            max_iter = int(self.param_widgets['max_iter'].text() or "100")

            if method == "Newton":
                try:
                    # Execute the Newton method
                    root, iterations = newton(f, df, x0, tol, max_iter)
                except ValueError as e:
                    error_msg = str(e)
            else:
                try:
                    # Execute the modified Newton method
                    root, iterations = modified_newton(f, df, ddf, x0, tol, max_iter)
                except ValueError as e:
                    error_msg = str(e)

        elif method == "Secant":
            x0 = float(self.param_widgets['x0'].text())
            x1 = float(self.param_widgets['x1'].text())
            plot_points.extend([x0, x1])
            tol = float(self.param_widgets['tol'].text() or "1e-5")
            max_iter = int(self.param_widgets['max_iter'].text() or "100")

            try:
                # Execute the Secant method
                root, iterations = secant(f, x0, x1, tol, max_iter)
            except ValueError as e:
                error_msg = str(e)

        results_msg = f"Root: {root}\nIterations: {iterations}"

        # Plot the graph
        self.plot_function_graph(python_expr, latex_expr)

        # Plotting parameters on the graph
        for idx, point in enumerate(plot_points):
            y_value = eval(python_expr, {
                "x": point,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "pi": math.pi,
                "e": math.e
            })
            # Limit to 2 decimal places
            self.graph_display.axes.scatter(point, y_value, color='#FFA500', s=50, zorder=2,
                                            label=f"Point {idx + 1}:({point:.2f}, {y_value:.2f})")

        # If root is found, plot it
        if root is not None:
            self.graph_display.axes.scatter(root, 0, color='#1E90FF', s=50, marker='x', zorder=3, label=f"Root: {root}")

        # Adjust the x-axis limits
        if root is not None:
            self.graph_display.axes.set_xlim(root - 2, root + 2)  # 2 units on either side of the root

        # Set the graph title based on dark mode

        if app.palette().color(QPalette.Window) == QColor(53, 53, 53):  # Dark mode
            self.graph_display.axes.set_title(f"Graph of ${latex_expr}$", color='white')
        else:  # Light mode
            self.graph_display.axes.set_title(f"Graph of ${latex_expr}$")

        # Set labels and legend to the top left
        self.graph_display.axes.legend(loc='upper left')

        # Allow legend to be draggable
        self.graph_display.axes.legend().set_draggable(True)

        # Refresh graph
        self.graph_display.draw()

        # Display results
        if error_msg:
            self.results_display.setText(f"Error: {error_msg}")
        else:
            self.results_display.setText(results_msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RootFinderApp()
    toggle_dark_mode()
    window.show()
    sys.exit(app.exec_())
