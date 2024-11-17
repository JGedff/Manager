from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

from utils.functions.globalFunctions import useLessFunction

from constants import FONT_SMALLEST_CHAR

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

        self.falseButton = QPushButton(falseString, self)

        self.trueButton.setFixedHeight(25)
        self.trueButton.setFont(FONT_SMALLEST_CHAR)
        self.trueButton.setStyleSheet("background-color: white; border: 1px solid #AFAFAF")

        self.falseButton.setFixedHeight(25)
        self.falseButton.setFont(FONT_SMALLEST_CHAR)
        self.falseButton.setStyleSheet("background-color: #A4F9FF; border: 1px solid #AFAFAF; border-right: 0px")

        # Add the icon and text to the layout
        layout.addWidget(self.trueButton)
        layout.addWidget(self.falseButton)

        layout.setSpacing(0)

    def initEvents(self):
        self.trueButton.clicked.connect(self.buttonTrueClicked)
        self.falseButton.clicked.connect(self.buttonFalseClicked)
    
    def buttonTrueClicked(self):
        self.value = True
        self.trueButton.setStyleSheet("background-color: #A4F9FF; border: 1px solid #AFAFAF; border-right: 0px")
        self.falseButton.setStyleSheet("background-color: white; border: 1px solid #AFAFAF")
        self.actionTrue()

    def buttonFalseClicked(self):
        self.value = False
        self.falseButton.setStyleSheet("background-color: #A4F9FF; border: 1px solid #AFAFAF")
        self.trueButton.setStyleSheet("background-color: white; border: 1px solid #AFAFAF; border-right: 0px")
        self.actionFalse()

    def getValue(self):
        return self.value
    
    def setValue(self, boolean):
        if boolean:
            self.buttonTrueClicked()
        else:
            self.buttonFalseClicked()