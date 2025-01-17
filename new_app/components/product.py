from utils.mongoDb import Mongo
from utils.user_manager import UserManager

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

from utils.language import Language

from constants import SHELVES, PRODUCTS_INFO

from styles.style_sheets import INPUT_TEXT, COMBO_BOX, REST_BUTTON, BLUE_BUTTON, EDIT_BUTTON, OFF_BUTTON, IMPORTANT_ACTION_BUTTON
from styles.fonts import FONT_SMALL_TEXT

from components.input_number import InputNumber
from components.inputNumberDecimal import InputNumberDecimal

class ProductManager():
    @staticmethod
    def add(name, price):
        PRODUCTS_INFO.append([name.capitalize(), price])
    
    @staticmethod
    def get(index):
        return PRODUCTS_INFO[index]
    
    @staticmethod
    def getByName(name):
        for prod in PRODUCTS_INFO:
            if prod[0] == name.capitalize():
                return prod
        
        return []

    @staticmethod
    def updateProduct(index, name, price):
        PRODUCTS_INFO[index][0] = name.capitalize()
        PRODUCTS_INFO[index][1] = price

    @staticmethod
    def updateProductName(index, name):
        PRODUCTS_INFO[index][0] = name.capitalize()

    @staticmethod
    def updateProductPrice(index, price):
        PRODUCTS_INFO[index][1] = price
    
    @staticmethod
    def getIndexByName(name):
        for i, prod in enumerate(PRODUCTS_INFO):
            if prod[0] == name:
                return i
        
        return -1

    @staticmethod
    def deleteByName(name):
        index = ProductManager.getIndexByName(name)

        if index != -1:
            PRODUCTS_INFO.pop(index)
    
    @staticmethod
    def countProducts():
        return PRODUCTS_INFO.__len__()

class Product(QLabel):
    def __init__(self, posX, posY, space, parent = None):
        super().__init__(parent)

        self.initVariables(posX, posY, space)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, posX, posY, space):
        self.spaceId = space.mongo_id
        self.edittingProduct = False
        self.creatingProduct = False
        self.products = []
        self.posX = posX
        self.posY = posY
        self.price = 0
        self.name = ''

        if UserManager.getUserRole() != 'Offline':
            self.products = Mongo.getMongoProducts()

            if self.products.__len__() < 1:
                QMessageBox.warning(None, "Products not found", "It will create the default products")

                self.addDefaultProducts()

                Mongo.addMongoProducts('Sock', 8)
                Mongo.addMongoProducts('Dress', 20)
                Mongo.addMongoProducts('Shirt', 30)
                Mongo.addMongoProducts('Jacket', 25)
                Mongo.addMongoProducts('Sweater', 35)

            else:
                for prod in self.products:
                    ProductManager.add(prod['name'], prod['price'])

        else:
            self.addDefaultProducts()
    
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

        self.edit_amount = InputNumber(1, True, parent)
        self.edit_amount.setGeometry(self.posX + 87, self.posY + 46, 175, 65)

        self.addProduct = QPushButton(Language.get("add_product"), parent)
        self.addProduct.setFont(FONT_SMALL_TEXT)
        self.addProduct.setStyleSheet(BLUE_BUTTON)
        self.addProduct.setGeometry(self.posX, self.posY + 125, 200, 25)

        self.labelNewProduct = QLabel(Language.get('product_name'), parent)
        self.labelNewProduct.setFont(FONT_SMALL_TEXT)
        self.labelNewProduct.setGeometry(self.posX, self.posY + 170, 212, 35)

        self.editNewName = QLineEdit(parent)
        self.editNewName.setFont(FONT_SMALL_TEXT)
        self.editNewName.setStyleSheet(INPUT_TEXT)
        self.editNewName.setPlaceholderText(Language.get("product"))
        self.editNewName.setGeometry(self.posX + 237, self.posY + 170, 150, 35)

        self.labelNewPrice = QLabel(Language.get('product_price'), parent)
        self.labelNewPrice.setFont(FONT_SMALL_TEXT)
        self.labelNewPrice.setGeometry(self.posX, self.posY + 230, 150, 35)

        self.editNewPrice = InputNumberDecimal(1, True, 2, parent)
        self.editNewPrice.setGeometry(self.posX + 87, self.posY + 215, 175, 65)

        self.cancelButtonAddProduct = QPushButton(Language.get("cancel"), parent)
        self.cancelButtonAddProduct.setFont(FONT_SMALL_TEXT)
        self.cancelButtonAddProduct.setStyleSheet(OFF_BUTTON)
        self.cancelButtonAddProduct.setGeometry(self.posX, self.posY + 125, 100, 25)
        self.cancelButtonAddProduct.hide()

        self.createProductButton = QPushButton(Language.get("create"), parent)
        self.createProductButton.setFont(FONT_SMALL_TEXT)
        self.createProductButton.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.createProductButton.setGeometry(self.posX + 237, self.posY + 300, 100, 25)
        self.createProductButton.hide()

        self.editProduct = QPushButton(Language.get('edit_product'), parent)
        self.editProduct.setFont(FONT_SMALL_TEXT)
        self.editProduct.setStyleSheet(EDIT_BUTTON)
        self.editProduct.setGeometry(self.posX + 237, self.posY + 125, 175, 25)

        self.editProductButton = QPushButton(Language.get("save"), parent)
        self.editProductButton.setFont(FONT_SMALL_TEXT)
        self.editProductButton.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.editProductButton.setGeometry(self.posX + 237, self.posY + 300, 100, 25)
        self.editProductButton.hide()

        self.cancelButtonEditProduct = QPushButton(Language.get("cancel"), parent)
        self.cancelButtonEditProduct.setFont(FONT_SMALL_TEXT)
        self.cancelButtonEditProduct.setStyleSheet(OFF_BUTTON)
        self.cancelButtonEditProduct.setGeometry(self.posX + 237, self.posY + 125, 100, 25)
        self.cancelButtonEditProduct.hide()

        self.editPrice = InputNumberDecimal(1, True, 2, parent)
        self.editPrice.setGeometry(self.posX + 87, self.posY + 215, 175, 65)
        self.editPrice.hide()

        self.labelEditProductName = QLabel(Language.get('edit_product_name'), parent)
        self.labelEditProductName.setFont(FONT_SMALL_TEXT)
        self.labelEditProductName.setGeometry(self.posX, self.posY + 170, 150, 35)
        self.labelEditProductName.hide()

        self.editProductName = QLineEdit(parent)
        self.editProductName.setFont(FONT_SMALL_TEXT)
        self.editProductName.setStyleSheet(INPUT_TEXT)
        self.editProductName.setPlaceholderText(Language.get("product"))
        self.editProductName.setGeometry(self.posX + 237, self.posY + 170, 150, 35)
        self.editProductName.hide()

        self.deleteProduct = QPushButton(Language.get('del_product'), parent)
        self.deleteProduct.setFont(FONT_SMALL_TEXT)
        self.deleteProduct.setStyleSheet(REST_BUTTON)
        self.deleteProduct.setGeometry(self.posX + 450, self.posY + 125, 175, 25)
        self.deleteProduct.hide()

        for item in self.products:
            self.selectProduct.addItem(item['name'])

        self.name = self.selectProduct.currentText()
        self.price = self.getActualProductPrice()

        self.priceLabel = QLabel(str(self.price) + " €", parent)
        self.priceLabel.setFont(FONT_SMALL_TEXT)
        self.priceLabel.setGeometry(self.posX + 252, self.posY + 5, 125, 30)

    def initEvents(self):
        self.editProductButton.clicked.connect(self.edit)
        self.editProduct.clicked.connect(self.showHideEdit)
        self.deleteProduct.clicked.connect(self.delProduct)
        self.editProductName.textChanged.connect(self.checkNewInfo)
        self.addProduct.clicked.connect(self.showHideCreateProduct)
        self.createProductButton.clicked.connect(self.createProduct)
        self.editNewName.textChanged.connect(self.enableCreateButton)
        self.editPrice.inputNum.textChanged.connect(self.checkNewInfo)
        self.cancelButtonEditProduct.clicked.connect(self.showHideEdit)
        self.edit_amount.get_input().textChanged.connect(self.updateBDspaceAmount)
        self.cancelButtonAddProduct.clicked.connect(self.showHideCreateProduct)
        self.selectProduct.currentTextChanged.connect(self.updateDBProductSpace)
    
    def addDefaultProducts(self):
        self.products.append({ "name": 'Sock', "price": 8 })
        self.products.append({ "name": 'Dress', "price": 20 })
        self.products.append({ "name": 'Shirt', "price": 30 })
        self.products.append({ "name": 'Jacket', "price": 25 })
        self.products.append({ "name": 'Sweater', "price": 35 })

        ProductManager.add('Sock', 8)
        ProductManager.add('Dress', 20)
        ProductManager.add('Shirt', 30)
        ProductManager.add('Jacket', 25)
        ProductManager.add('Sweater', 35)

    def getActualProductPrice(self):
        productName = self.selectProduct.currentText()
        product = ProductManager.getByName(productName)

        return product[1]

    def edit(self):
        self.showHideEdit()
        
        if self.price != self.editPrice.get_value() and (self.name != self.editProductName.text().capitalize() and self.editProductName.text().strip() != ""):
            index = ProductManager.getIndexByName(self.name)

            if index != -1:
                ProductManager.updateProduct(index, self.editProductName.text(), self.editPrice.get_value())

                if UserManager.getUserRole() != 'Offline':
                    Mongo.updateMongoProduct(self.name, self.editProductName.text(), self.editPrice.get_value())

                self.name = self.editProductName.text()
                self.price = self.editPrice.get_value()

                self.selectProduct.setItemText(self.selectProduct.currentIndex(), self.name.capitalize())
                self.priceLabel.setText(str(self.price) + " €")

        elif self.name != self.editProductName.text().capitalize() and self.editProductName.text().strip() != "":
            index = ProductManager.getIndexByName(self.name)

            if index != -1:
                ProductManager.updateProductName(index, self.editProductName.text())

                if UserManager.getUserRole() != 'Offline':
                    Mongo.updateMongoProductName(self.name, self.editProductName.text())

                self.name = self.editProductName.text()

                self.selectProduct.setItemText(self.selectProduct.currentIndex(), self.name.capitalize())

        elif self.price != self.editPrice.get_value():
            index = ProductManager.getIndexByName(self.name)

            if index != -1:
                ProductManager.updateProductPrice(index, self.editPrice.get_value())

                if UserManager.getUserRole() != 'Offline':
                    Mongo.updateMongoProductPrice(self.name, self.editPrice.get_value())

                self.price = self.editPrice.get_value()

                self.priceLabel.setText(str(self.price) + " €")

        else:
            QMessageBox.warning(None, "Update failed", "Price or name must be diferent from the actual values")

        self.editProductName.setText("")

    def showHideEdit(self):
        if self.edittingProduct:
            self.addProduct.setDisabled(False)
            self.editProduct.setDisabled(False)
            self.deleteProduct.setDisabled(False)

            self.editProduct.setGeometry(self.posX + 237, self.posY + 125, self.editProduct.width(), self.editProduct.height())

            self.editPrice.hide()
            self.labelNewPrice.hide()
            self.editProductName.hide()
            self.labelEditProductName.hide()

            self.editProductButton.hide()
            self.cancelButtonEditProduct.hide()
        else:
            self.addProduct.setDisabled(True)
            self.editProduct.setDisabled(True)
            self.deleteProduct.setDisabled(True)

            self.editProduct.setGeometry(self.posX, self.posY + 300, self.editProduct.width(), self.editProduct.height())
            self.editPrice.setValue(self.price)

            self.editPrice.show()
            self.labelNewPrice.show()
            self.editProductName.show()
            self.editProductButton.show()
            self.labelEditProductName.show()
            self.cancelButtonEditProduct.show()
            self.editProductButton.setDisabled(True)
        
        self.edittingProduct = not self.edittingProduct
    
    def delProduct(self):
        if ProductManager.countProducts() <= 2:
            self.deleteProduct.setDisabled(True)

        if UserManager.getUserRole != 'Offline':
            Mongo.delMongoProduct(self.name)

        ProductManager.deleteByName(self.name)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if isinstance(space.product, Product):
                        spaceIndex = space.product.selectProduct.findText(self.name)

                        if spaceIndex != -1:
                            space.product.selectProduct.removeItem(spaceIndex)

                            space.product.name = space.product.selectProduct.currentText()
                            space.product.price = space.product.getActualProductPrice()

    def checkNewInfo(self):
        if self.price != self.editPrice.get_value():
            self.editProductButton.setDisabled(False)
        elif self.name != self.editProductName.text().capitalize() and self.editProductName.text().strip() != "":
            self.editProductButton.setDisabled(False)
        else:
            self.editProductButton.setDisabled(True)

    def updateDBProductSpace(self):
        if UserManager.getUserRole() != 'Offline':
            Mongo.updateMongoSpaceProduct(self.spaceId, self.selectProduct.currentText())

        self.name = self.selectProduct.currentText()
        self.price = self.getActualProductPrice()

        self.priceLabel.setText(str(self.price) + " €")

        if self.edittingProduct:
            self.showHideEdit()

    def updateBDspaceAmount(self):
        if UserManager.getUserRole() != 'Offline':
            Mongo.updateMongoSpaceAmount(self.spaceId, self.edit_amount.get_value())
    
    def createProduct(self):
        if ProductManager.countProducts() > 1:
            self.deleteProduct.setDisabled(False)

        if UserManager.getUserRole() != 'Offline':
            Mongo.addMongoProducts(self.editNewName.text(), self.editNewPrice.get_value())
        
        ProductManager.add(self.editNewName.text(), self.editNewPrice.get_value())
        
        self.showHideCreateProduct()

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if isinstance(space.product, Product):
                        space.product.selectProduct.addItem(self.editNewName.text().capitalize())

    def showHideCreateProduct(self):
        if self.creatingProduct:
            self.addProduct.setDisabled(False)
            self.editProduct.setDisabled(False)
            self.deleteProduct.setDisabled(False)

            self.addProduct.setGeometry(self.posX, self.posY + 125, 200, 25)

            self.editNewName.hide()
            self.editNewPrice.hide()
            self.labelNewPrice.hide()
            self.labelNewProduct.hide()
            self.createProductButton.hide()
            self.cancelButtonAddProduct.hide()
        else:
            self.addProduct.setDisabled(True)
            self.editProduct.setDisabled(True)
            self.deleteProduct.setDisabled(True)
            self.createProductButton.setDisabled(True)

            self.addProduct.setGeometry(self.posX, self.posY + 300, 200, 25)

            self.editNewPrice.setValue(1.0)
            self.editNewName.setText("")

            self.editNewName.show()
            self.editNewPrice.show()
            self.labelNewPrice.show()
            self.labelNewProduct.show()
            self.createProductButton.show()
            self.cancelButtonAddProduct.show()

        self.creatingProduct = not self.creatingProduct
    
    def enableCreateButton(self):
        if self.editNewName.text().__len__() > 0:
            self.createProductButton.setDisabled(False)
        else:
            self.createProductButton.setDisabled(True)

    def show(self):
        super().show()

        self.edit_amount.show()
        self.priceLabel.show()
        self.labelAmount.show()
        self.labelProduct.show()
        self.selectProduct.show()

        if UserManager.getUserRole() == 'Manager' or UserManager.getUserRole() == 'Product' or UserManager.getUserRole() == 'Offline':
            self.addProduct.show()
            self.editProduct.show()
            self.deleteProduct.show()

    def hide(self):
        super().hide()

        self.edit_amount.hide()
        self.addProduct.hide()
        self.priceLabel.hide()
        self.editProduct.hide()
        self.labelAmount.hide()
        self.editNewName.hide()
        self.editNewPrice.hide()
        self.labelProduct.hide()
        self.deleteProduct.hide()
        self.labelNewPrice.hide()
        self.selectProduct.hide()
        self.labelNewProduct.hide()
        
        if self.creatingProduct:
            self.showHideCreateProduct()
        elif self.edittingProduct:
            self.showHideEdit()
