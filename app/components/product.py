from utils.mongoDb import Mongo
from utils.userManager import UserManager

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QColorDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

from utils.language import Language

from styles.styleSheets import INPUT_TEXT, DEFAULT_BUTTON, COMBO_BOX, REST_BUTTON, BLUE_BUTTON, EDIT_BUTTON, OFF_BUTTON, REGISTER_BUTTON, IMPORTANT_ACTION_BUTTON, BACKGROUND_BLACK, BACKGROUND_GREY
from styles.fonts import FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR, FONT_SMALL_BOLD_TEXT, FONT_BOLD_TITLE
from styles.colorFunctions import getStyleSheet

from components.inputNumber import InputNumber

class Product(QLabel):
    def __init__(self, posX, posY, parent = None):
        super().__init__(parent)

        self.initVariables(posX, posY)
        self.initUI(parent)

    def initVariables(self, posX, posY):
        self.products = []
        self.posX = posX
        self.posY = posY
        self.amount = 0
        self.price = 0
        self.name = ''

        if UserManager.getUserRole() != 'Offline':
            self.products = Mongo.getMongoProducts()

            if self.products.__len__() < 1:
                QMessageBox.warning(None, "Products not found", "It will create the default products")

                self.products.append({ "name": 'Sock' })
                self.products.append({ "name": 'Dress' })
                self.products.append({ "name": 'Jacket' })
                self.products.append({ "name": 'Shirt' })
                self.products.append({ "name": 'Sweater' })

                Mongo.addMongoProducts('Sock', 8)
                Mongo.addMongoProducts('Shirt', 20)
                Mongo.addMongoProducts('Dress', 25)
                Mongo.addMongoProducts('Sweater', 30)
                Mongo.addMongoProducts('Jacket', 35)

        else:
            self.products.append({ "name": 'Sock' })
            self.products.append({ "name": 'Dress' })
            self.products.append({ "name": 'Jacket' })
            self.products.append({ "name": 'Shirt' })
            self.products.append({ "name": 'Sweater' })

            QMessageBox.information(None, "You're offline", "It will load the default products")

    def initUI(self, parent):
        self.labelProduct = QLabel(Language.get('product'), parent)
        self.labelProduct.setFont(FONT_SMALL_TEXT)
        self.labelProduct.setGeometry(self.posX, self.posY + 5, 150, 35)

        self.labelAmount = QLabel(Language.get('amount'), parent)
        self.labelAmount.setFont(FONT_SMALL_TEXT)
        self.labelAmount.setGeometry(self.posX, self.posY + 60, 150, 35)

        self.selectProduct = QComboBox(parent)
        self.selectProduct.setFont(FONT_SMALL_TEXT)
        self.selectProduct.setStyleSheet(COMBO_BOX)
        self.selectProduct.setGeometry(self.posX + 96, self.posY + 6, 125, 30)

        for item in self.products:
            self.selectProduct.addItem(item['name'])

        self.editAmount = InputNumber(1, True, parent)
        self.editAmount.setGeometry(self.posX + 87, self.posY + 46, 175, 65)

    def show(self):
        super().show()

        self.editAmount.show()
        self.labelAmount.show()
        self.labelProduct.show()
        self.selectProduct.show()

    def hide(self):
        super().hide()

        self.editAmount.hide()
        self.labelAmount.hide()
        self.labelProduct.hide()
        self.selectProduct.hide()