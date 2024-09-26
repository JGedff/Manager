from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

class DoubleButton(QLabel):
    def __init__(self, posx, posy, textbutton1, textButton2, functionButton1, functionButton2, parent = None):
        super().__init__(parent)

        self.setGeometry(posx - 12, posy - 12, 450, 50)

        self.initUI(posx, posy, textbutton1, textButton2, parent)
        self.initEvents(functionButton1, functionButton2)

    def initUI(self, posx, posy, textButton1, textButton2, parent):
        # Create a layout for the button to hold icon and text
        layout = QHBoxLayout(self)

        # Create and set the icon image
        self.button1 = QPushButton(textButton1, parent)
        self.button1.setGeometry(posx, posy, 0, 0)
        self.button1.setStyleSheet("width: 200px; height: 19px")

        self.button2 = QPushButton(textButton2, parent)
        self.button2.setGeometry(posx + 225, posy, 0, 0)
        self.button2.setStyleSheet("margin-left: 5px; width: 50px; height: 25px")

        if textButton2 == "":
            self.button2.hide()

        # Add the icon and text to the layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.setSpacing(0)

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