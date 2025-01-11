from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

from styles.styleSheets import INPUT_NUMBER, ADD_BUTTON, REST_BUTTON, NO_RIGHT_BORDER_BUTTON, NO_RIGHT_BORDER_BUTTON_INPUT
from styles.fonts import FONT_SMALLEST_CHAR

from utils.functions.checkFunctions import checkIsDecimal

class InputNumberDecimal(QLabel):
    def __init__(self, defaultNumber = 0, writeNumber = False, maxDecimals = 2, parent = None):
        super().__init__(parent)

        self.initVariables(defaultNumber, maxDecimals)
        self.initUI(not writeNumber)
        self.initEvents()
    
    def initVariables(self, defaultNumber, maxDecimals):
        self.defaultNumber = defaultNumber
        self.lastNumber = defaultNumber
        self.maxDecimals = maxDecimals

    def initUI(self, writeNumber):
        layout = QHBoxLayout(self)

        self.inputNum = QLineEdit(self)
        self.inputNum.setText(str(self.defaultNumber))
        self.inputNum.setReadOnly(writeNumber)

        self.addNumber = QPushButton("↑", self)

        self.restNumber = QPushButton("↓", self)

        layout.addWidget(self.addNumber)
        layout.addWidget(self.inputNum)
        layout.addWidget(self.restNumber)

        self.inputNum.setFixedHeight(50)
        self.inputNum.setFont(FONT_SMALLEST_CHAR)
        self.inputNum.setStyleSheet(INPUT_NUMBER + NO_RIGHT_BORDER_BUTTON_INPUT)

        self.addNumber.setFixedWidth(50)
        self.addNumber.setFixedHeight(50)
        self.addNumber.setFont(FONT_SMALLEST_CHAR)
        self.addNumber.setStyleSheet(ADD_BUTTON + NO_RIGHT_BORDER_BUTTON)

        self.restNumber.setFixedWidth(50)
        self.restNumber.setFixedHeight(50)
        self.restNumber.setFont(FONT_SMALLEST_CHAR)
        self.restNumber.setStyleSheet(REST_BUTTON)

        layout.setSpacing(0)
    
    def initEvents(self):
        self.addNumber.clicked.connect(self.addNum)
        self.restNumber.clicked.connect(self.restNum)
        self.inputNum.textChanged.connect(self.checkNumber)

    def addNum(self):
        actualNum = self.inputNum.text()
        self.inputNum.setText(str(float(actualNum) + 1))

    def restNum(self):
        actualNum = self.inputNum.text()
    
        if float(actualNum) > self.defaultNumber:
            self.inputNum.setText(str(float(actualNum) - 1))

    def checkNumber(self):
        textToCheck = self.inputNum.text()
        decimals = textToCheck.split(".")

        if decimals.__len__() >= 2 and decimals[1].__len__() > self.maxDecimals:
            textToCheck = decimals[0] + "." + decimals[1][0] + decimals[1][1]

        isNumber = checkIsDecimal(textToCheck)

        if textToCheck == "" or not isNumber or float(textToCheck) < self.defaultNumber:
            self.inputNum.setText(str(self.lastNumber))
        else:
            self.lastNumber = textToCheck
            self.inputNum.setText(str(textToCheck))

    def setValue(self, num):
        if num >= self.defaultNumber:
            self.lastNumber = num
            self.inputNum.setText(str(self.lastNumber))

    def getNum(self):
        return float(self.inputNum.text())