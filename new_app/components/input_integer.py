from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

from styles.style_sheets import INPUT_NUMBER, ADD_BUTTON, REST_BUTTON, NO_RIGHT_BORDER_BUTTON, NO_RIGHT_BORDER_BUTTON_INPUT
from styles.fonts import FONT_SMALLEST_CHAR

from utils.functions.checkFunctions import is_num

class InputInteger(QLabel):
    def __init__(self, min = 0, write_number = False, parent = None):
        super().__init__(parent)

        self.init_variables(min)
        self.init_ui(not write_number)
        self.init_events()
    
    def init_variables(self, min):
        self._min = min
        self._last_number = str(min)

    def init_ui(self, write_number):
        # Create buttons
        self._add_one_button = QPushButton("↑", self)
        self._add_one_button.setFixedWidth(50)
        self._add_one_button.setFixedHeight(50)

        self._rest_one_button = QPushButton("↓", self)
        self._rest_one_button.setFixedWidth(50)
        self._rest_one_button.setFixedHeight(50)

        # Create input
        self._input = QLineEdit(self)
        self._input.setFixedHeight(50)
        self._input.setText(str(self._min))
        self._input.setReadOnly(write_number)

        # Style buttons
        self._add_one_button.setFont(FONT_SMALLEST_CHAR)
        self._add_one_button.setStyleSheet(ADD_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self._rest_one_button.setFont(FONT_SMALLEST_CHAR)
        self._rest_one_button.setStyleSheet(REST_BUTTON)

        # Style input
        self._input.setFont(FONT_SMALLEST_CHAR)
        self._input.setStyleSheet(INPUT_NUMBER + NO_RIGHT_BORDER_BUTTON_INPUT)

        # Create layout
        layout = QHBoxLayout(self)

        # Add buttons and input to layout
        layout.addWidget(self._add_one_button)
        layout.addWidget(self._input)
        layout.addWidget(self._rest_one_button)
        
        # Style layout
        layout.setSpacing(0)
    
    def init_events(self):
        self._input.textChanged.connect(self.format_value)
        self._add_one_button.clicked.connect(self.add_num_input)
        self._rest_one_button.clicked.connect(self.rest_num_input)

    def add_num_input(self):
        # Get the number of the input
        actual_num = self._input.text()

        # Add one to that number and put it on the input
        self._input.setText(str(int(actual_num) + 1))

    def rest_num_input(self):
        actual_num = self._input.text()
    
        # If the actual number is greather than the minimum number, rest one
        if int(actual_num) > self._min:
            self._input.setText(str(int(actual_num) - 1))

    def format_value(self):
        new_value = self._input.text()

        # If the new text is empty, is not a number, or is less than the minimum, keep the last value
        if new_value == "" or not is_num(new_value):
            self._input.setText(self._last_number)

        # If the new value is less than the minimum, keep the minimum
        elif int(new_value) < self._min:
            self._last_number = self._min

            self._input.setText(self._min)
        
        # If the new text is diferent than the last number, keep the new value
        elif new_value != self._last_number:
            self._last_number = new_value

            self._input.setText(new_value)

    def set_value(self, number):
        if number >= self._min:
            self._input.setText(str(self._last_number))

    def get_value(self):
        return int(self._input.text())
    
    def get_input(self):
        return self._input