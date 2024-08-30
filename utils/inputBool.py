from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

class InputBool(QLabel):
    def __init__(self, trueString, falseString, actionTrue, actionFalse, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.trueButton = QPushButton(trueString, self)
        self.trueButton.clicked.connect(actionTrue)

        self.falseButton = QPushButton(falseString, self)
        self.falseButton.clicked.connect(actionFalse)

        self.trueButton.setStyleSheet("background-color: #ebebeb")
        self.falseButton.setStyleSheet("background-color: #4fd9ff")

        # Add the icon and text to the layout
        layout.addWidget(self.trueButton)
        layout.addWidget(self.falseButton)

        layout.setSpacing(0)