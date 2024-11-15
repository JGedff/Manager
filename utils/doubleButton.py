from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5.QtCore import QRect, QPoint

from constants import FONT_SMALL_TEXT

class DoubleButton(QLabel):
    def __init__(self, textbutton1, textButton2, functionButton1, functionButton2, parent = None):
        super().__init__(parent)

        self.initUI(textbutton1, textButton2, parent)
        self.initEvents(functionButton1, functionButton2)

    def initUI(self, textButton1, textButton2, parent):
        # Create a layout for the button to hold icon and text
        self.widget = QWidget(parent)

        # Create and set the icon image
        self.button1 = QPushButton(textButton1, self.widget)
        self.button1.setGeometry(25, 13, 250, 39)

        self.button2 = QPushButton(textButton2, self.widget)
        self.button2.setGeometry(300, 13, 50, 39)

        self.button1.setFont(FONT_SMALL_TEXT)
        self.button2.setFont(FONT_SMALL_TEXT)

        self.button1.setStyleSheet("background-color: white; border: 1px solid #CACACA")
        self.button2.setStyleSheet("background-color: #FFD1D1; border: 1px solid #FFA1A1")

    def initEvents(self, functionButton1, functionButton2):
        self.button1.clicked.connect(functionButton1)
        self.button2.clicked.connect(functionButton2)
    
    def textButton1(self):
        return self.button1.text()

    def textButton2(self):
        return self.button2.text()

    def setTextButton1(self, value):
        self.button1.setText(value)

    def setTextButton2(self, value):
        self.button2.setText(value)
        
    def setDisabledButton1(self, value):
        self.button1.setDisabled(value)

    def setDisabledButton2(self, value):
        self.button2.setDisabled(value)

    def setGeometry(self, x, y, width, height):
        super().setGeometry(x, y, width, height)
        self.widget.setGeometry(QRect(x, y, width, height))

    def hide(self):
        super().hide()
        self.widget.hide()

        self.button1.hide()
        self.button2.hide()

    def show(self):
        super().show()
        self.widget.show()

        self.button1.show()
        self.button2.show()

    def raise_(self):
        self.button1.raise_()
        self.button2.raise_()

    def move(self, x, y):
        super().move(x, y)
        self.widget.move(QPoint(x, y))

        self.button1.move(QPoint(x + self.button1.x(), y + self.button1.y()))
        self.button2.move(QPoint(x + self.button2.x(), y + self.button2.y()))
