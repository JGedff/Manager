from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageButton(QPushButton):
    def __init__(self, text, icon_path, parent = None):
        super().__init__(parent)

        self.initUI(text, icon_path)

    def initUI(self, text, icon_path):
        # Create a layout for the button to hold icon and text
        layout = QVBoxLayout(self)

        # Create and set the icon image
        icon_label = QLabel(self)
        pixmap = QPixmap(icon_path)
        icon_label.setPixmap(pixmap)
        icon_label.setScaledContents(True)
        icon_label.setAlignment(Qt.AlignCenter)

        # Create and set the text label
        text_label = QLabel(text, self)
        text_label.setAlignment(Qt.AlignCenter)

        # Add the icon and text to the layout
        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        layout.setSpacing(5)
