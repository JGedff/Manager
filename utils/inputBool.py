from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

from utils.functions.globalFunctions import useLessFunction

class InputBool(QLabel):
    def __init__(self, trueString, falseString, parent = None, actionTrue = useLessFunction, actionFalse = useLessFunction):
        super().__init__(parent)

        self.initVariables(actionTrue, actionFalse)
        self.initUI(trueString, falseString)
        self.initEvents()

    def initVariables(self, actionTrue, actionFalse):
        self.value = False

        self.actionTrue = actionTrue
        self.actionFalse = actionFalse

    def initUI(self, trueString, falseString):
        layout = QHBoxLayout(self)

        self.trueButton = QPushButton(trueString, self)
        self.trueButton.setStyleSheet("background-color: #ebebeb")

        self.falseButton = QPushButton(falseString, self)
        self.falseButton.setStyleSheet("background-color: #4fd9ff")

        # Add the icon and text to the layout
        layout.addWidget(self.trueButton)
        layout.addWidget(self.falseButton)

        layout.setSpacing(0)

    def initEvents(self):
        self.trueButton.clicked.connect(self.buttonTrueClicked)
        self.falseButton.clicked.connect(self.buttonFalseClicked)
    
    def buttonTrueClicked(self):
        self.value = True
        self.trueButton.setStyleSheet("background-color: #4fd9ff")
        self.falseButton.setStyleSheet("background-color: #ebebeb")
        self.actionTrue()

    def buttonFalseClicked(self):
        self.value = False
        self.falseButton.setStyleSheet("background-color: #4fd9ff")
        self.trueButton.setStyleSheet("background-color: #ebebeb")
        self.actionFalse()

    def getValue(self):
        return self.value
