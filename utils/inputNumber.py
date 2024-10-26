from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

from utils.functions.checkFunctions import checkIsNum

class InputNumber(QLabel):
    def __init__(self, defaultNumber = 0, writeNumber = False, parent = None):
        super().__init__(parent)

        self.initVariables(defaultNumber)
        self.initUI(not writeNumber)
        self.initEvents()
    
    def initVariables(self, defaultNumber):
        self.defaultNumber = defaultNumber
        self.lastNumber = defaultNumber

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

        layout.setSpacing(0)
    
    def initEvents(self):
        self.addNumber.clicked.connect(self.addNum)
        self.restNumber.clicked.connect(self.restNum)
        self.inputNum.textChanged.connect(self.checkNumber)

    def addNum(self):
        actualNum = self.inputNum.text()
        self.inputNum.setText(str(int(actualNum) + 1))

    def restNum(self):
        actualNum = self.inputNum.text()
    
        if int(actualNum) > self.defaultNumber:
            self.inputNum.setText(str(int(actualNum) - 1))

    def checkNumber(self):
        textToCheck = self.inputNum.text()
        isNumber = checkIsNum(textToCheck)

        if textToCheck == "" or not isNumber or int(textToCheck) < self.defaultNumber:
            self.inputNum.setText(str(self.lastNumber))
        else:
            self.lastNumber = textToCheck

    def setValue(self, num):
        if num >= self.defaultNumber:
            self.lastNumber = num
            self.inputNum.setText(str(self.lastNumber))

    def getNum(self):
        return int(float(self.inputNum.text()))