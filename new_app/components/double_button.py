from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5.QtCore import QRect, QPoint

from styles.style_sheets import DEFAULT_BUTTON, REST_BUTTON
from styles.fonts import FONT_SMALL_TEXT

class DoubleButton(QLabel):
    def __init__(self, text_first_button: str, text_second_button: str, function_first_button, funciton_second_button, parent = None):
        super().__init__(parent)

        self.init_ui(text_first_button, text_second_button, parent)
        self.init_events(function_first_button, funciton_second_button)

    def init_ui(self, text_first_button: str, text_second_button: str, parent):
        # Create a layout for the button to hold icon and text
        self.widget = QWidget(parent)

        # Create buttons
        self._first_button = QPushButton(text_first_button, self.widget)
        self._first_button.setGeometry(25, 13, 250, 39)

        self._second_button = QPushButton(text_second_button, self.widget)
        self._second_button.setGeometry(300, 13, 50, 39)

        # Style buttons
        self._first_button.setFont(FONT_SMALL_TEXT)
        self._second_button.setFont(FONT_SMALL_TEXT)

        self._first_button.setStyleSheet(DEFAULT_BUTTON)
        self._second_button.setStyleSheet(REST_BUTTON)

    def init_events(self, function_first_button, funciton_second_button):
        self._first_button.clicked.connect(function_first_button)
        self._second_button.clicked.connect(funciton_second_button)
    
    def get_first_button_text(self):
        return self._first_button.text()

    def get_second_button_text(self):
        return self._second_button.text()

    def set_first_button_text(self, text: str):
        self._first_button.setText(text)

    def set_second_button_text(self, text: str):
        self._second_button.setText(text)
        
    def set_first_button_disabled(self, disabled: bool):
        self._first_button.setDisabled(disabled)

    def set_second_button_disabled(self, disabled: bool):
        self._second_button.setDisabled(disabled)

    def setGeometry(self, x: int, y: int, width: int, height: int):
        super().setGeometry(x, y, width, height)
        self.widget.setGeometry(QRect(x, y, width, height))

    def hide(self):
        super().hide()
        self.widget.hide()

        self._first_button.hide()
        self._second_button.hide()

    def show(self):
        super().show()
        self.widget.show()

        self._first_button.show()
        self._second_button.show()

    def raise_(self):
        self._first_button.raise_()
        self._second_button.raise_()

    def move(self, x: int, y: int):
        super().move(x, y)
        self.widget.move(QPoint(x, y))

        self._first_button.move(QPoint(x + self._first_button.x(), y + self._first_button.y()))
        self._second_button.move(QPoint(x + self._second_button.x(), y + self._second_button.y()))

    def get_first_button_sender_text(self) -> str:
        # The sender function acts as a click listener
        return self._first_button.sender().text()
    
    def get_second_button(self):
        return self._second_button
