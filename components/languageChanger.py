from PyQt5.QtWidgets import QLabel, QComboBox

from utils.language import Language

from constants import WINDOW_HEIGHT

class LanguageChanger(QLabel):
    def __init__(self, window, parent):
        super().__init__(parent)

        self.initVariables(window)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, window):
        self.WINDOW = window

    def initUI(self,parent):
        self.changer = QComboBox(parent)
        self.changer.addItem("English")
        self.changer.addItem("Español")
        self.changer.addItem("Català")
        self.changer.setGeometry(15, WINDOW_HEIGHT - 50, 100, 25)
    
    def initEvents(self):
        self.changer.currentTextChanged.connect(self.changeLang)

    def changeLang(self):
        Language.changeTo(self.changer.currentText())
        self.updateUI()

    def updateUI(self):
        # Window global info
        self.WINDOW.setWindowTitle(Language.get("window_title"))

        # Window button names
        self.WINDOW.addStoreButton.setText(Language.get("add_store"))