from utils.mongoDb import Mongo
from utils.userManager import UserManager

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QColorDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

from utils.language import Language

from styles.styleSheets import INPUT_TEXT, DEFAULT_BUTTON, COMBO_BOX, REST_BUTTON, BLUE_BUTTON, EDIT_BUTTON, OFF_BUTTON, REGISTER_BUTTON, IMPORTANT_ACTION_BUTTON, BACKGROUND_BLACK, BACKGROUND_GREY
from styles.fonts import FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR, FONT_SMALL_BOLD_TEXT, FONT_BOLD_TITLE
from styles.colorFunctions import getStyleSheet

from components.inputNumber import InputNumber
from components.inputNumberDecimal import InputNumberDecimal

class Product(QLabel):
    def __init__(self, posX, posY, space, parent = None):
        super().__init__(parent)

        self.initVariables(posX, posY, space)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, posX, posY, space):
        self.creatingProduct = False
        self.SPACE = space
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

        self.addProduct = QPushButton(Language.get("add_product"), parent)
        self.addProduct.setFont(FONT_SMALL_TEXT)
        self.addProduct.setStyleSheet(BLUE_BUTTON)
        self.addProduct.setGeometry(self.posX, self.posY + 100, 200, 25)

        self.labelNewProduct = QLabel(Language.get('product_name'), parent)
        self.labelNewProduct.setFont(FONT_SMALL_TEXT)
        self.labelNewProduct.setGeometry(self.posX, self.posY + 145, 150, 35)

        self.editNewName = QLineEdit(parent)
        self.editNewName.setFont(FONT_SMALL_TEXT)
        self.editNewName.setStyleSheet(INPUT_TEXT)
        self.editNewName.setPlaceholderText(Language.get("product"))
        self.editNewName.setGeometry(self.posX, self.posY + 145, 150, 35)

        self.labelNewPrice = QLabel(Language.get('product_price'), parent)
        self.labelNewPrice.setFont(FONT_SMALL_TEXT)
        self.labelNewPrice.setGeometry(self.posX, self.posY + 200, 150, 35)

        self.editNewPrice = InputNumberDecimal(1, True, parent)
        self.editNewPrice.setGeometry(self.posX + 87, self.posY + 46, 175, 65)

        self.cancelButtonAddProduct = QPushButton(Language.get("cancel"), parent)
        self.cancelButtonAddProduct.setFont(FONT_SMALL_TEXT)
        self.cancelButtonAddProduct.setStyleSheet(OFF_BUTTON)
        self.cancelButtonAddProduct.setGeometry(self.posX + 87, self.posY + 46, 175, 65)

        self.createProductButton = QPushButton(Language.get("create"), parent)
        self.createProductButton.setFont(FONT_SMALL_TEXT)
        self.createProductButton.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.createProductButton.setGeometry(self.posX + 438, self.posY, 100, 25)

    def initEvents(self):
        self.addProduct.clicked.connect(self.showHideCreateProduct)
        self.createProductButton.clicked.connect(self.createProduct)
        self.editAmount.inputNum.textChanged.connect(self.updateBDspaceAmount)
        self.cancelButtonAddProduct.clicked.connect(self.showHideCreateProduct)
        self.selectProduct.currentTextChanged.connect(self.updateDBProductSpace)

    def updateDBProductSpace(self):
        if UserManager.getUserRole() != 'Offline':
            Mongo.updateMongoSpaceProduct(self.SPACE.mongo_id, self.selectProduct.currentText())

    def updateBDspaceAmount(self):
        if UserManager.getUserRole() != 'Offline':
            Mongo.updateMongoSpaceAmount(self.SPACE.mongo_id, self.editAmount.inputNum)
    
    def createProduct(self):
        if UserManager.getUserRole() != 'Offline':
            Mongo.addMongoProducts(self.editNewName, self.editNewPrice)

    def showHideCreateProduct(self):
        if self.creatingProduct:
            self.editNewName.hide()
            self.editNewPrice.hide()
            self.labelNewPrice.hide()
            self.labelNewProduct.hide()
            self.createProductButton.hide()
        else:
            self.editNewName.show()
            self.editNewPrice.show()
            self.labelNewPrice.show()
            self.labelNewProduct.show()
            self.createProductButton.show()

        self.creatingProduct = not self.creatingProduct

    def show(self):
        super().show()

        self.editAmount.show()
        self.addProduct.show()
        self.labelAmount.show()
        self.labelProduct.show()
        self.selectProduct.show()

    def hide(self):
        super().hide()

        self.editAmount.hide()
        self.addProduct.hide()
        self.labelAmount.hide()
        self.editNewName.hide()
        self.editNewPrice.hide()
        self.labelProduct.hide()
        self.labelNewPrice.hide()
        self.selectProduct.hide()
        self.labelNewProduct.hide()