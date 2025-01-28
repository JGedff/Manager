from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from styles.style_sheets import IMAGE_BUTTON
from styles.fonts import FONT_SMALL_TEXT

class ImageButton(QPushButton):
    def __init__(self, text: str, icon_path: str, parent: QWidget | None = None):
        super().__init__(parent)

        self.init_ui(text, icon_path)

    def init_ui(self, text: str, icon_path: str):
        # Create image
        pixmap = QPixmap(icon_path)

        ## INITIALIZE OBJECTS ##
        # Labels
        # Label with pixmap (image)
        self._icon_image = QLabel(self)
        self._icon_image.setPixmap(pixmap)
        self._icon_image.setScaledContents(True)
        self._icon_image.setAlignment(Qt.AlignCenter)

        self._text_label = QLabel(text, self)
        self._text_label.setFont(FONT_SMALL_TEXT)
        self._text_label.setAlignment(Qt.AlignCenter)

        ## STYLE ##
        self.setStyleSheet(IMAGE_BUTTON)

        ## LAYOUT ##
        layout = QVBoxLayout(self)

        # Add icon and text to the layout
        layout.addWidget(self._icon_image)
        layout.addWidget(self._text_label)

        # Style layout
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)

    def text(self):
        return self._text_label.text()

    def setText(self, text: str):
        self._text_label.setText(text)

    def setPixmap(self, icon_path: str):
        pixmap = QPixmap(icon_path)

        self._icon_image.setPixmap(pixmap)
