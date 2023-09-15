import io
import re
import sys
import sympy as sp
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt


def preprocess_input(expression):
    """
    Preprocess the expression to handle implicit multiplications.
    e.g. "2x" becomes "2*x".
    """
    # Use a regex to find all instances of a number followed by a letter (e.g., "2x")
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

    return expression


def convert_to_latex(expression):
    """
    Convert a plain text mathematical expression to LaTeX format using SymPy.
    """
    # Preprocess the expression to handle implicit multiplications
    expression = preprocess_input(expression)

    # Convert to SymPy expression
    expr = sp.sympify(expression)

    # Convert to LaTeX
    latex_expr = sp.latex(expr, mul_symbol='dot')

    # Post-process: Remove any unwanted 'cdot' to handle implicit multiplications
    latex_expr = latex_expr.replace('\\cdot', '')

    return latex_expr


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
        method_label = QLabel("Methods:")
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["Bisection", "False Position", "Modified Newton", "Newton", "Secant"])
        self.calculate_button = QPushButton("Calculate")

        input_layout.addWidget(self.fx_input)
        input_layout.addWidget(method_label)
        input_layout.addWidget(self.method_dropdown)
        input_layout.addWidget(self.calculate_button)
        main_layout.addLayout(input_layout)

        # Distinguish the clear button using QPushButton
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("background-color: red; color: white; border: none;")
        clear_button.clicked.connect(self.fx_input.clear)
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

        # Results Display (placeholder for now)
        self.results_display = QTextEdit()
        self.results_display.setPlaceholderText("Results will be displayed here...")
        main_layout.addWidget(self.results_display)

        # Graph Visualization (placeholder for now)
        self.graph_display = QTextEdit()
        self.graph_display.setPlaceholderText("Graph will be displayed here...")

        # Using QSplitter to allow resizing sections
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(main_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.graph_display)

        self.setCentralWidget(splitter)

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
            latex_expr = convert_to_latex(expression)
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

        except Exception as e:
            # If there's any error in rendering, display an error message directly without any LaTeX wrapping
            self.error_display_label.setText(f"Your current input is invalid:\n{str(e)}")
            self.fx_input.setStyleSheet("border: 2px solid red;")  # Set input border to red


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RootFinderApp()
    toggle_dark_mode()
    window.show()
    sys.exit(app.exec_())
