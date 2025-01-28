from utils.mongo_db import Mongo
from utils.user_manager import UserManager

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

from utils.language import Language
from utils.product_manager import ProductManager

from constants import SHELVES

from styles.style_sheets import INPUT_TEXT, COMBO_BOX, REST_BUTTON, BLUE_BUTTON, EDIT_BUTTON, OFF_BUTTON, IMPORTANT_ACTION_BUTTON
from styles.fonts import FONT_SMALL_TEXT

from components.input_integer import InputInteger
from components.input_float import InputFloat

class Product(QLabel):
    @staticmethod
    def update_all_product_selector_name(old_name: str, new_name: str):
        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if hasattr(space, "product") and isinstance(space.product, Product):
                        for i in range(space.product.select_product.count()):
                            if space.product.select_product.itemText(i) == old_name:
                                space.product.select_product.setItemText(i, new_name)

    def __init__(self, pos_x: int, pos_y: int, space, parent: QWidget | None = None):
        super().__init__(parent)

        self.init_variables(pos_x, pos_y, space)
        self.init_ui(parent)
        self.init_events()

    def init_variables(self, pos_x: int, pos_y: int, space):
        self._space_id = space.mongo_id
        self.editting_product = False
        self.creating_product = False
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._price = 0
        self._name = ''

        self._products = list()

        if UserManager.get_role() != 'Offline':
            self.add_db_products()
        else:
            self.add_default_products()

    def add_db_products(self):
        self._products = Mongo.get_products()

        if len(self._products) < 1:
            QMessageBox.warning(None, "Products not found", "It will create the default products")

            self.add_default_products()

            Mongo.add_product('Sock', 8)
            Mongo.add_product('Dress', 20)
            Mongo.add_product('Shirt', 30)
            Mongo.add_product('Jacket', 25)
            Mongo.add_product('Sweater', 35)

        else:
            for db_products in self._products:
                ProductManager.add(db_products['name'], db_products['price'])            

    def add_default_products(self):
        if ProductManager.count() < 1:
            self._products.append({ "name": 'Sock', "price": 8 })
            self._products.append({ "name": 'Dress', "price": 20 })
            self._products.append({ "name": 'Shirt', "price": 30 })
            self._products.append({ "name": 'Jacket', "price": 25 })
            self._products.append({ "name": 'Sweater', "price": 35 })

            ProductManager.add('Sock', 8)
            ProductManager.add('Dress', 20)
            ProductManager.add('Shirt', 30)
            ProductManager.add('Jacket', 25)
            ProductManager.add('Sweater', 35)
        else:
            product_list = ProductManager.get_all_products()

            for prod in product_list:
                self._products.append({ "name": prod[0], "price": prod[1] })

    def init_ui(self, parent: QWidget | None):
        ## INITIALIZE OBJECTS ##
        # Labels
        self.label_product = QLabel(Language.get('product'), parent)
        self.label_product.setGeometry(self._pos_x, self._pos_y + 5, 150, 35)

        self.label_amount = QLabel(Language.get('amount'), parent)
        self.label_amount.setGeometry(self._pos_x, self._pos_y + 60, 150, 35)

        self.label_new_product = QLabel(Language.get('product_name'), parent)
        self.label_new_product.setGeometry(self._pos_x, self._pos_y + 170, 212, 35)

        self.label_new_price = QLabel(Language.get('product_price'), parent)
        self.label_new_price.setGeometry(self._pos_x, self._pos_y + 230, 150, 35)

        self.label_edit_product_name = QLabel(Language.get('edit_product_name'), parent)
        self.label_edit_product_name.setGeometry(self._pos_x, self._pos_y + 170, 150, 35)
        self.label_edit_product_name.hide()

        # Buttons
        self.cancel_add_product_button = QPushButton(Language.get("cancel"), parent)
        self.cancel_add_product_button.setGeometry(self._pos_x, self._pos_y + 125, 100, 25)
        self.cancel_add_product_button.hide()

        self.add_product_button = QPushButton(Language.get("add_product"), parent)
        self.add_product_button.setGeometry(self._pos_x, self._pos_y + 125, 200, 25)

        self.create_product_button = QPushButton(Language.get("create"), parent)
        self.create_product_button.setGeometry(self._pos_x + 237, self._pos_y + 300, 100, 25)
        self.create_product_button.hide()

        self.edit_product = QPushButton(Language.get('edit_product'), parent)
        self.edit_product.setGeometry(self._pos_x + 237, self._pos_y + 125, 175, 25)

        self.edit_product_button = QPushButton(Language.get("save"), parent)
        self.edit_product_button.setGeometry(self._pos_x + 237, self._pos_y + 300, 100, 25)
        self.edit_product_button.hide()

        self.cancel_button_edit_product = QPushButton(Language.get("cancel"), parent)
        self.cancel_button_edit_product.setGeometry(self._pos_x + 237, self._pos_y + 125, 100, 25)
        self.cancel_button_edit_product.hide()

        self.delete_product = QPushButton(Language.get('del_product'), parent)
        self.delete_product.setGeometry(self._pos_x + 450, self._pos_y + 125, 175, 25)
        self.delete_product.hide()

        # Inputs
        self.edit_amount = InputInteger(1, True, parent)
        self.edit_amount.setGeometry(self._pos_x + 87, self._pos_y + 46, 175, 65)

        self.edit_new_name = QLineEdit(parent)
        self.edit_new_name.setPlaceholderText(Language.get("product"))
        self.edit_new_name.setGeometry(self._pos_x + 237, self._pos_y + 170, 150, 35)

        self.edit_new_price = InputFloat(1, True, 2, parent)
        self.edit_new_price.setGeometry(self._pos_x + 87, self._pos_y + 215, 175, 65)

        self.edit_price = InputFloat(1, True, 2, parent)
        self.edit_price.setGeometry(self._pos_x + 87, self._pos_y + 215, 175, 65)
        self.edit_price.hide()

        self.edit_product_name = QLineEdit(parent)
        self.edit_product_name.setPlaceholderText(Language.get("product"))
        self.edit_product_name.setGeometry(self._pos_x + 237, self._pos_y + 170, 150, 35)
        self.edit_product_name.hide()

        # Others
        self.select_product = QComboBox(parent)
        self.select_product.setGeometry(self._pos_x + 96, self._pos_y + 6, 125, 30)

        for item in self._products:
            self.select_product.addItem(item['name'])

        self._name = self.select_product.currentText()
        self._price = self.get_actual_product_price()

        # This label is here, because needs the QComboBox initialized in order to get the price of the product
        self.label_price = QLabel(str(self._price) + " €", parent)
        self.label_price.setGeometry(self._pos_x + 252, self._pos_y + 5, 125, 30)

        ## STYLES ##
        # Labels
        self.label_price.setFont(FONT_SMALL_TEXT)
        self.label_amount.setFont(FONT_SMALL_TEXT)
        self.label_product.setFont(FONT_SMALL_TEXT)
        self.label_new_price.setFont(FONT_SMALL_TEXT)
        self.label_new_product.setFont(FONT_SMALL_TEXT)
        self.label_edit_product_name.setFont(FONT_SMALL_TEXT)

        # Buttons
        self.create_product_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.create_product_button.setFont(FONT_SMALL_TEXT)

        self.edit_product_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.edit_product_button.setFont(FONT_SMALL_TEXT)

        self.cancel_button_edit_product.setStyleSheet(OFF_BUTTON)
        self.cancel_button_edit_product.setFont(FONT_SMALL_TEXT)

        self.cancel_add_product_button.setStyleSheet(OFF_BUTTON)
        self.cancel_add_product_button.setFont(FONT_SMALL_TEXT)

        self.add_product_button.setStyleSheet(BLUE_BUTTON)
        self.add_product_button.setFont(FONT_SMALL_TEXT)

        self.delete_product.setStyleSheet(REST_BUTTON)
        self.delete_product.setFont(FONT_SMALL_TEXT)

        self.edit_product.setStyleSheet(EDIT_BUTTON)
        self.edit_product.setFont(FONT_SMALL_TEXT)

        # Inputs
        self.edit_new_name.setFont(FONT_SMALL_TEXT)
        self.edit_new_name.setStyleSheet(INPUT_TEXT)

        self.edit_product_name.setFont(FONT_SMALL_TEXT)
        self.edit_product_name.setStyleSheet(INPUT_TEXT)

        # Others
        self.select_product.setFont(FONT_SMALL_TEXT)
        self.select_product.setStyleSheet(COMBO_BOX)

    def get_actual_product_price(self) -> float:
        product_name = self.select_product.currentText()
        product = ProductManager.get_by_name(product_name)

        if len(product) > 1:
            return product[1]
        
        return 0.0

    def init_events(self):
        self.edit_product_button.clicked.connect(self.edit)
        self.edit_product.clicked.connect(self.show_hide_edit)
        self.add_product_button.clicked.connect(self.show_hide_create)
        self.delete_product.clicked.connect(self.del_product_function)
        self.cancel_button_edit_product.clicked.connect(self.show_hide_edit)
        self.cancel_add_product_button.clicked.connect(self.show_hide_create)
        self.create_product_button.clicked.connect(self.create_product_function)
        self.edit_new_name.textChanged.connect(self.enable_disable_create_button)
        self.select_product.currentTextChanged.connect(self.update_db_product_space)
        self.edit_product_name.textChanged.connect(self.enable_disable_update_button)
        self.edit_amount.get_input().textChanged.connect(self.update_bd_space_amount)
        self.edit_price.get_input().textChanged.connect(self.enable_disable_update_button)

    def edit(self):
        self.show_hide_edit()

        # If the price saved is diferent than the price in the input AND the name saved is diferent from the name in the input and is not an empty string
        if self._price != self.edit_price.get_value() and (self._name != self.edit_product_name.text().capitalize() and self.edit_product_name.text().strip() != ""):
            index = ProductManager.get_index_by_name(self._name)

            if index != -1:
                self.update_name_price(index)

        # If the name saved is diferent from the name in the input and is not an empty string
        elif self._name != self.edit_product_name.text().capitalize() and self.edit_product_name.text().strip() != "":
            index = ProductManager.get_index_by_name(self._name)

            if index != -1:
                self.update_name(index)

        elif self._price != self.edit_price.get_value():
            index = ProductManager.get_index_by_name(self._name)

            if index != -1:
                self.update_price(index)

        else:
            QMessageBox.warning(None, "Update failed", "Price or name must be diferent from the actual values")

        self.edit_product_name.setText("")

    def show_hide_edit(self):
        if self.editting_product:
            # Disable buttons
            self.add_product_button.setDisabled(False)
            self.delete_product.setDisabled(False)
            self.edit_product.setDisabled(False)

            self.edit_product.setGeometry(self._pos_x + 237, self._pos_y + 125, self.edit_product.width(), self.edit_product.height())

            # Hide edit elements
            self.edit_price.hide()
            self.label_new_price.hide()
            self.edit_product_name.hide()
            self.edit_product_button.hide()
            self.label_edit_product_name.hide()
            self.cancel_button_edit_product.hide()

        else:
            # Enable buttons
            self.add_product_button.setDisabled(True)
            self.edit_product.setDisabled(True)
            self.delete_product.setDisabled(True)

            self.edit_product.setGeometry(self._pos_x, self._pos_y + 300, self.edit_product.width(), self.edit_product.height())
            self.edit_price.set_value(self._price)

            # Show edit elements
            self.edit_price.show()
            self.label_new_price.show()
            self.edit_product_name.show()
            self.edit_product_button.show()
            self.label_edit_product_name.show()
            self.cancel_button_edit_product.show()
            self.edit_product_button.setDisabled(True)

        self.editting_product = not self.editting_product

    def update_name_price(self, index: int):
        # Update the information in the db and local
        ProductManager.update_product(index, self.edit_product_name.text(), self.edit_price.get_value())

        Product.update_all_product_selector_name(self._name, self.edit_product_name.text())

        if UserManager.get_role() != 'Offline':
            Mongo.update_product(self._name, self.edit_product_name.text(), self.edit_price.get_value())

        # Update properties
        self._name = self.edit_product_name.text().capitalize()
        self._price = self.edit_price.get_value()

        # Update labels and dropdown
        self.select_product.setItemText(self.select_product.currentIndex(), self._name.capitalize())
        self.label_price.setText(str(self._price) + " €")

    def update_name(self, index: int):
        # Update the information in the db and local
        ProductManager.update_product_name(index, self.edit_product_name.text())

        Product.update_all_product_selector_name(self._name, self.edit_product_name.text())

        if UserManager.get_role() != 'Offline':
            Mongo.update_product_name(self._name, self.edit_product_name.text())

        # Update name property
        self._name = self.edit_product_name.text().capitalize()

        # Update product dropdown
        self.select_product.setItemText(self.select_product.currentIndex(), self._name.capitalize())

    def update_price(self, index: int):
        # Update the information in the db and local
        ProductManager.update_product_price(index, self.edit_price.get_value())

        if UserManager.get_role() != 'Offline':
            Mongo.update_product_price(self._name, self.edit_price.get_value())

        # Update price property
        self._price = self.edit_price.get_value()

        # Update price label
        self.label_price.setText(str(self._price) + " €")

    def del_product_function(self):
        # Disable delete button if there are two or less products
        if ProductManager.count() <= 2:
            self.delete_product.setDisabled(True)

        # Delete the actual product in db and local
        if UserManager.get_role() != 'Offline':
            Mongo.del_product(self._name)

        ProductManager.delete_by_name(self._name)

        # Update all spaces with products
        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    # If the space has a product
                    if hasattr(space, "product") and isinstance(space.product, Product):
                        index = space.product.select_product.findText(self._name)

                        if index != -1:
                            # Remove the product from the dropdown
                            space.product.select_product.removeItem(index)

                            # Update the name and price of the space product
                            space.product._name = space.product.select_product.currentText()
                            space.product._price = space.product.get_actual_product_price()

    def enable_disable_update_button(self):
        if self._price != self.edit_price.get_value():
            self.edit_product_button.setDisabled(False)
        elif self._name != self.edit_product_name.text().capitalize() and self.edit_product_name.text().strip() != "":
            self.edit_product_button.setDisabled(False)
        else:
            self.edit_product_button.setDisabled(True)

    def update_db_product_space(self):
        # Update the space, so now, it holds the new product
        if UserManager.get_role() != 'Offline':
            Mongo.update_space_product(self._space_id, self.select_product.currentText())

        # Update the name and price of the product
        self._name = self.select_product.currentText()
        self._price = self.get_actual_product_price()

        self.label_price.setText(str(self._price) + " €")

        if self.editting_product:
            self.show_hide_edit()

    def update_bd_space_amount(self):
        # Update the space amount
        if UserManager.get_role() != 'Offline':
            Mongo.update_space_amount(self._space_id, self.edit_amount.get_value())
    
    def create_product_function(self):
        if ProductManager.count() > 1:
            self.delete_product.setDisabled(False)

        if UserManager.get_role() != 'Offline':
            Mongo.add_product(self.edit_new_name.text(), self.edit_new_price.get_value())
        
        ProductManager.add(self.edit_new_name.text(), self.edit_new_price.get_value())
        
        self.show_hide_create()

        # Add the new product in the dropdown of every space that has a product
        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if hasattr(space, "product") and isinstance(space.product, Product):
                        space.product.select_product.addItem(self.edit_new_name.text().capitalize())

    def show_hide_create(self):
        if self.creating_product:
            # Enable buttons
            self.edit_product.setDisabled(False)
            self.delete_product.setDisabled(False)
            self.add_product_button.setDisabled(False)

            self.add_product_button.setGeometry(self._pos_x, self._pos_y + 125, 200, 25)

            # Hide elements
            self.edit_new_name.hide()
            self.edit_new_price.hide()
            self.label_new_price.hide()
            self.label_new_product.hide()
            self.create_product_button.hide()
            self.cancel_add_product_button.hide()
        else:
            # Disable elements
            self.edit_product.setDisabled(True)
            self.delete_product.setDisabled(True)
            self.add_product_button.setDisabled(True)
            self.create_product_button.setDisabled(True)

            self.add_product_button.setGeometry(self._pos_x, self._pos_y + 300, 200, 25)

            # Reset the edit product inputs
            self.edit_new_price.set_value(1.0)
            self.edit_new_name.setText("")

            # Show elements
            self.edit_new_name.show()
            self.edit_new_price.show()
            self.label_new_price.show()
            self.label_new_product.show()
            self.create_product_button.show()
            self.cancel_add_product_button.show()

        self.creating_product = not self.creating_product
    
    def enable_disable_create_button(self):
        if len(self.edit_new_name.text().strip()) > 0:
            self.create_product_button.setDisabled(False)
        else:
            self.create_product_button.setDisabled(True)

    def show(self):
        super().show()

        self.label_price.show()
        self.edit_amount.show()
        self.label_amount.show()
        self.label_product.show()
        self.select_product.show()

        self._name = self.select_product.currentText()
        self._price = self.get_actual_product_price()

        # If the user has not any of those roles, should be unable to see or press the next buttons
        if UserManager.get_role() == 'Manager' or UserManager.get_role() == 'Product' or UserManager.get_role() == 'Offline':
            self.add_product_button.show()
            self.delete_product.show()
            self.edit_product.show()

    def hide(self):
        super().hide()

        self.label_price.hide()
        self.edit_amount.hide()
        self.edit_product.hide()
        self.label_amount.hide()
        self.edit_new_name.hide()
        self.label_product.hide()
        self.delete_product.hide()
        self.select_product.hide()
        self.edit_new_price.hide()
        self.label_new_price.hide()
        self.label_new_product.hide()
        self.add_product_button.hide()

        if self.creating_product:
            self.show_hide_create()
        elif self.editting_product:
            self.show_hide_edit()
