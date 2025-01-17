from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

from styles.style_sheets import INPUT_NUMBER, ADD_BUTTON, REST_BUTTON, NO_RIGHT_BORDER_BUTTON, NO_RIGHT_BORDER_BUTTON_INPUT
from styles.fonts import FONT_SMALLEST_CHAR

from utils.functions.checkFunctions import is_decimal

class InputDecimal(QLabel):
    def __init__(self, min = 0, write_number = False, max_decimals = 2, parent = None):
        super().__init__(parent)

        self.init_variables(min, max_decimals)
        self.init_ui(not write_number)
        self.init_events()
    
    def init_variables(self, min, max_decimals):
        self._min = min
        self._last_number = str(min)
        self._max_decimals = max_decimals

    def init_ui(self, write_number):
        # Create input
        self._input = QLineEdit(self)
        self._input.setFixedHeight(50)
        self._input.setText(str(self._min))
        self._input.setReadOnly(write_number)

        # Create buttons
        self._add_one_button = QPushButton("↑", self)
        self._add_one_button.setFixedWidth(50)
        self._add_one_button.setFixedHeight(50)

        self._rest_one_button = QPushButton("↓", self)
        self._rest_one_button.setFixedWidth(50)
        self._rest_one_button.setFixedHeight(50)

        # Style buttons
        self._add_one_button.setFont(FONT_SMALLEST_CHAR)
        self._add_one_button.setStyleSheet(ADD_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self._rest_one_button.setFont(FONT_SMALLEST_CHAR)
        self._rest_one_button.setStyleSheet(REST_BUTTON)

        # Create layout
        layout = QHBoxLayout(self)

        # Add input and buttons to layout
        layout.addWidget(self._add_one_button)
        layout.addWidget(self._input)
        layout.addWidget(self._rest_one_button)

        # Style input
        self._input.setFont(FONT_SMALLEST_CHAR)
        self._input.setStyleSheet(INPUT_NUMBER + NO_RIGHT_BORDER_BUTTON_INPUT)

        layout.setSpacing(0)
    
    def init_events(self):
        self._add_one_button.clicked.connect(self.add_one)
        self._input.textChanged.connect(self.format_value)
        self._rest_one_button.clicked.connect(self.rest_one)

    def add_one(self):
        actual_num = self._input.text()
        self._input.setText(str(float(actual_num) + 1))

    def format_value(self):
        new_value = self._input.text()
        decimals = new_value.split(".")

        # If it has decimals and there are more decimals than the maximum decimals, keep the decimals until it reach the maximum
        if decimals.__len__() >= 2 and decimals[1].__len__() > self._max_decimals:
            new_value = decimals[0] + "."

            for i in range(self._max_decimals):
                new_value += decimals[1][i]

        if new_value == "" or not is_decimal(new_value):
            self._input.setText(self._last_number)

        # If the new value is less than the minimum, keep the minimum
        elif float(new_value) < self._min:
            self._last_number = self._min

            self._input.setText(self._min)

        elif new_value != self._last_number:
            self._last_number = new_value

            self._input.setText(new_value)

    def rest_one(self):
        actual_num = self._input.text()
    
        if float(actual_num) > self._min:
            self._input.setText(str(float(actual_num) - 1))

    def set_value(self, num):
        if num >= self._min:
            self._input.setText(str(num))

    def get_value(self):
        return float(self._input.text())
    
    def get_input(self):
        return self._input