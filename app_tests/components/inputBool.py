from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

from app_tests.styles.styleSheets import TRUE_BUTTON, FALSE_BUTTON, NO_RIGHT_BORDER_BUTTON
from app_tests.styles.fonts import FONT_SMALLEST_CHAR

from app_tests.utils.functions.globalFunctions import useLessFunction

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
        self.trueButton.setStyleSheet(FALSE_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self.falseButton.setFixedHeight(25)
        self.falseButton.setFont(FONT_SMALLEST_CHAR)
        self.falseButton.setStyleSheet(TRUE_BUTTON)

        # Add the icon and text to the layout
        layout.addWidget(self.trueButton)
        layout.addWidget(self.falseButton)

        layout.setSpacing(0)

    def initEvents(self):
        self.trueButton.clicked.connect(self.buttonTrueClicked)
        self.falseButton.clicked.connect(self.buttonFalseClicked)
    
    def buttonTrueClicked(self):
        self.value = True

        self.trueButton.setStyleSheet(TRUE_BUTTON + NO_RIGHT_BORDER_BUTTON)
        
        self.falseButton.setStyleSheet(FALSE_BUTTON)

        self.actionTrue()

    def buttonFalseClicked(self):
        self.value = False

        self.falseButton.setStyleSheet(TRUE_BUTTON)

        self.trueButton.setStyleSheet(FALSE_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self.actionFalse()

    def getValue(self):
        return self.value
    
    def setValue(self, boolean):
        if boolean:
            self.buttonTrueClicked()
        else:
            self.buttonFalseClicked()