from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from styles.style_sheets import IMAGE_BUTTON
from styles.fonts import FONT_SMALL_TEXT

class ImageButton(QPushButton):
    def __init__(self, text, icon_path, parent = None):
        super().__init__(parent)

        self.init_ui(text, icon_path)

    def init_ui(self, text, icon_path):
        # Create a layout for the button to hold icon and text
        self._layout = QVBoxLayout(self)

        # Create image
        pixmap = QPixmap(icon_path)

        # Create icon image
        self._icon_image = QLabel(self)
        self._icon_image.setPixmap(pixmap)
        self._icon_image.setScaledContents(True)
        self._icon_image.setAlignment(Qt.AlignCenter)

        # Create text label
        self._text_label = QLabel(text, self)
        self._text_label.setFont(FONT_SMALL_TEXT)
        self._text_label.setAlignment(Qt.AlignCenter)

        # Add icon and text to the layout
        self._layout.addWidget(self._icon_image)
        self._layout.addWidget(self._text_label)

        # Style icon
        self._layout.setAlignment(Qt.AlignCenter)
        self._layout.setSpacing(5)
        self.setStyleSheet(IMAGE_BUTTON)

    def text(self):
        return self._text_label.text()

    def setText(self, text):
        self._text_label.setText(text)

    def setPixmap(self, icon):
        pixmap = QPixmap(icon)

        self._icon_image.setPixmap(pixmap)
