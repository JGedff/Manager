from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

from styles.style_sheets import INPUT_NUMBER, ADD_BUTTON, REST_BUTTON, NO_RIGHT_BORDER_BUTTON, NO_RIGHT_BORDER_BUTTON_INPUT
from styles.fonts import FONT_SMALLEST_CHAR

from utils.functions.checkFunctions import is_num

class InputNumber(QLabel):
    def __init__(self, min = 0, writeNumber = False, parent = None):
        super().__init__(parent)

        self.init_variables(min)
        self.init_ui(not writeNumber)
        self.init_events()
    
    def init_variables(self, min):
        self._min = min
        self._last_number = str(min)

    def init_ui(self, writeNumber):
        # Create layout
        layout = QHBoxLayout(self)

        # Create buttons
        self._add_number = QPushButton("↑", self)
        self._add_number.setFixedWidth(50)
        self._add_number.setFixedHeight(50)

        self._rest_number = QPushButton("↓", self)
        self._rest_number.setFixedWidth(50)
        self._rest_number.setFixedHeight(50)

        # Create input
        self._input_num = QLineEdit(self)
        self._input_num.setFixedHeight(50)
        self._input_num.setText(str(self._min))
        self._input_num.setReadOnly(writeNumber)

        # Style buttons
        self._add_number.setFont(FONT_SMALLEST_CHAR)
        self._add_number.setStyleSheet(ADD_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self._rest_number.setFont(FONT_SMALLEST_CHAR)
        self._rest_number.setStyleSheet(REST_BUTTON)

        # Style input
        self._input_num.setFont(FONT_SMALLEST_CHAR)
        self._input_num.setStyleSheet(INPUT_NUMBER + NO_RIGHT_BORDER_BUTTON_INPUT)

        # Add buttons and input to layout
        layout.addWidget(self._add_number)
        layout.addWidget(self._input_num)
        layout.addWidget(self._rest_number)
        
        # Style layout
        layout.setSpacing(0)
    
    def init_events(self):
        self._add_number.clicked.connect(self.add_num_input)
        self._rest_number.clicked.connect(self.rest_num_input)
        self._input_num.textChanged.connect(self.format_value)

    def add_num_input(self):
        # Get the number of the input
        actual_num = self._input_num.text()

        # Add one to that number and put it on the input
        self._input_num.setText(str(int(actual_num) + 1))

    def rest_num_input(self):
        actual_num = self._input_num.text()
    
        # If the actual number is greather than the minimum number, rest one
        if int(actual_num) > self._min:
            self._input_num.setText(str(int(actual_num) - 1))

    def format_value(self):
        new_value = self._input_num.text()
        is_number = is_num(new_value)

        # If the new text is empty, is not a number, or is less than the minimum, keep the last value
        if new_value == "" or not is_number or int(new_value) < self._min:
            self._input_num.setText(self._last_number)
        
        # If the new text is diferent than the last number, keep the new value
        elif new_value != self._last_number:
            self._last_number = new_value
            self._input_num.setText(new_value)

    def set_value(self, number):
        if number >= self._min:
            self._input_num.setText(str(self._last_number))

    def get_value(self):
        return int(self._input_num.text())
    
    def get_input(self):
        return self._input_num