from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

from styles.style_sheets import TRUE_BUTTON, FALSE_BUTTON, NO_RIGHT_BORDER_BUTTON
from styles.fonts import FONT_SMALLEST_CHAR

from utils.functions.global_functions import useless_function

class InputBool(QLabel):
    def __init__(self, true_text: str, false_text: str, parent = None, true_action = useless_function, false_action = useless_function):
        super().__init__(parent)

        self.init_variables(true_action, false_action)
        self.init_ui(true_text, false_text)
        self.init_events()

    def init_variables(self, true_action, false_action):
        self._value = False

        self._true_action = true_action
        self._false_action = false_action

    def init_ui(self, true_text: str, false_text: str):
        ## INITIALIZE OBJECTS ##
        # Buttons
        self._true_button = QPushButton(true_text, self)
        self._true_button.setFixedHeight(25)

        self._false_button = QPushButton(false_text, self)
        self._false_button.setFixedHeight(25)

        ## STYLE ##
        # Buttons
        self._true_button.setFont(FONT_SMALLEST_CHAR)
        self._true_button.setStyleSheet(FALSE_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self._false_button.setFont(FONT_SMALLEST_CHAR)
        self._false_button.setStyleSheet(TRUE_BUTTON)

        ## LAYOUT ##
        layout = QHBoxLayout(self)

        # Add buttons to the layout
        layout.addWidget(self._true_button)
        layout.addWidget(self._false_button)

        # Change spacing between buttons
        layout.setSpacing(0)

    def init_events(self):
        self._true_button.clicked.connect(self.true_function)
        self._false_button.clicked.connect(self.false_function)
    
    def true_function(self):
        if not self._value:
            self._value = True

            # Change style, so user knows which button is on
            self._true_button.setStyleSheet(TRUE_BUTTON + NO_RIGHT_BORDER_BUTTON)
            self._false_button.setStyleSheet(FALSE_BUTTON)

            self._true_action()

    def false_function(self):
        if self._value:
            self._value = False

            # Change style, so user knows which button is on
            self._false_button.setStyleSheet(TRUE_BUTTON)
            self._true_button.setStyleSheet(FALSE_BUTTON + NO_RIGHT_BORDER_BUTTON)

            self._false_action()

    def get_value(self):
        return self._value
    
    def set_value(self, new_value: bool):
        if new_value:
            self.true_function()
        else:
            self.false_function()
    
    def set_true_text(self, text: str):
        self._true_button.setText(text)

    def set_false_text(self, text: str):
        self._false_button.setText(text)
    
    def set_true_button_disabled(self, disabled: bool):
        self._true_button.setDisabled(disabled)

    def set_false_button_disabled(self, disabled: bool):
        self._false_button.setDisabled(disabled)
