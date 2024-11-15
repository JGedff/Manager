from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from constants import FONT_SMALL_TEXT

class ImageButton(QPushButton):
    def __init__(self, text, icon_path, parent = None, resetButton = False):
        super().__init__(parent)

        self.initVariables(resetButton)
        self.initUI(text, icon_path)

    def initVariables(self, resetButton):
        self.resetButton = resetButton

    def initUI(self, text, icon_path):
        # Create a layout for the button to hold icon and text
        self.myLayout = QVBoxLayout(self)

        # Create and set the icon image
        pixmap = QPixmap(icon_path)
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setScaledContents(True)
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Create and set the text label
        self.text_label = QLabel(text, self)
        self.text_label.setFont(FONT_SMALL_TEXT)
        self.text_label.setAlignment(Qt.AlignCenter)

        # Add the icon and text to the layout
        self.myLayout.addWidget(self.icon_label)
        self.myLayout.addWidget(self.text_label)

        self.myLayout.setAlignment(Qt.AlignCenter)
        self.myLayout.setSpacing(5)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #CACACA;
            }
        """)

    def text(self):
        return self.text_label.text()

    def setText(self, text):
        self.text_label.setText(text)

    def setPixmap(self, icon):
        pixmap = QPixmap(icon)
        self.icon_label.setPixmap(pixmap)
