from PyQt5.QtWidgets import QLabel, QComboBox

from styles.style_sheets import COMBO_BOX
from styles.fonts import FONT_SMALL_TEXT

from constants import WINDOW_HEIGHT, STORES, SHELVES_FORMS, SHELVES

from utils.language import Language

from components.product import Product

class LanguageChanger(QLabel):
    def __init__(self, window, parent):
        super().__init__(parent)

        self.init_variables(window)
        self.init_ui(parent)
        self.init_events()

    def init_variables(self, window):
        self.language = 'English'
        self.WINDOW = window

    def init_ui(self,parent):
        self.changer = QComboBox(parent)
        self.changer.addItem("English")
        self.changer.addItem("Español")
        self.changer.addItem("Català")

        self.changer.setFont(FONT_SMALL_TEXT)
        self.changer.setGeometry(15, WINDOW_HEIGHT - 50, 100, 25)
        self.changer.setStyleSheet(COMBO_BOX)
    
    def init_events(self):
        self.changer.currentTextChanged.connect(self.change_lang)

    def change_lang(self, language):
        Language.changeTo(language)

        self.update_ui()
        self.language = language

    def update_ui(self):
        try:
            self.WINDOW.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))
            self.WINDOW.createStoreButton.setText(Language.get("create_store"))
            self.WINDOW.editCategories.setText(Language.get("edit_categories"))
            self.WINDOW.setDefaultIcon.setText(Language.get("default_image"))
            self.WINDOW.formStoreIcon.setText(Language.get("change_image"))
            self.WINDOW.storeNameLabel.setText(Language.get("name_store"))
            self.WINDOW.addStoreButton.setText(Language.get("add_store"))
            self.WINDOW.addShelfButton.setText(Language.get("add_shelf"))
            self.WINDOW.setWindowTitle(Language.get("window_title"))
            self.WINDOW.goHome.setText(Language.get("go_back"))

            self.WINDOW.categoryManager.showSpace.setText(Language.get("go_back"))
            self.WINDOW.categoryManager.saveCategory.setText(Language.get("save"))
            self.WINDOW.categoryManager.addCategory.setText(Language.get("add_category"))
            self.WINDOW.categoryManager.categoryColor.setText(Language.get("select_color"))
            self.WINDOW.categoryManager.createCategoryButton.setText(Language.get("create"))
            self.WINDOW.categoryManager.cancelButtonAddCategory.setText(Language.get("cancel"))
            self.WINDOW.categoryManager.categoryNameLabel.setText(Language.get("category_name"))
            self.WINDOW.categoryManager.addCategoryName.setPlaceholderText(Language.get("name"))
            self.WINDOW.categoryManager.categoryColorLabel.setText(Language.get("category_color"))
            self.WINDOW.categoryManager.newCategoryColorButton.setText(Language.get("select_color"))
            
            # Shelf forms
            for shelfIndex, shelf in enumerate(SHELVES_FORMS):
                shelf.shelfLabel.setText(Language.get("shelf") + str(shelfIndex + 1))
                shelf.inputSpacesLabel.setText(Language.get("shelf_question_1"))
                shelf.doubleShelfLabel.setText(Language.get("shelf_question_2"))
                shelf.shelfFloorsLabel.setText(Language.get("shelf_question_4"))
                shelf.doubleShelfInput.setTrueButtonText(Language.get("yes"))
                shelf.doubleShelfInput.setFalseButtonText(Language.get("no"))

            # Stores
            for store in STORES:
                store.goBackStore.setText(Language.get("go_back"))
                store.changeFloorButton.clear()

                for index in range(store.floor):
                    store.changeFloorButton.addItem(Language.get("floor") + str(index + 1))

            # Shelf
            for storage in SHELVES:
                for shelf in storage:
                    shelf.shelfNumber.setText(Language.get("shelf") + str(shelf.actualNumber) + ":")

                    # Space
                    for space in shelf.spaces:
                        space.shelfNumber.setText(Language.get("shelf") + str(space.shelfIndex + 1) + ":")
                        space.labelCategoryHoldProduct.setText(Language.get("category_hold_product"))
                        space.changeCategoryHoldProduct.setTrueButtonText(Language.get("yes"))
                        space.changeCategoryHoldProduct.setFalseButtonText(Language.get("no"))
                        space.openSpaceConfig.setText(Language.get("go_back"))
                        space.labelCategory.setText(Language.get("category"))

                        space.category.showSpace.setText(Language.get("go_back"))
                        space.category.saveCategory.setText(Language.get("save"))
                        space.category.addCategory.setText(Language.get("add_category"))
                        space.category.categoryColor.setText(Language.get("select_color"))
                        space.category.createCategoryButton.setText(Language.get("create"))
                        space.category.cancelButtonAddCategory.setText(Language.get("cancel"))
                        space.category.categoryNameLabel.setText(Language.get("category_name"))
                        space.category.addCategoryName.setPlaceholderText(Language.get("name"))
                        space.category.categoryColorLabel.setText(Language.get("category_color"))
                        space.category.newCategoryColorButton.setText(Language.get("select_color"))

                        if isinstance(space.product, Product):
                            space.product.labelEditProductName.setText(Language.get('edit_product_name'))
                            space.product.editProductName.setPlaceholderText(Language.get("product"))
                            space.product.editNewName.setPlaceholderText(Language.get("product"))
                            space.product.cancelButtonEditProduct.setText(Language.get("cancel"))
                            space.product.cancelButtonAddProduct.setText(Language.get("cancel"))
                            space.product.labelNewProduct.setText(Language.get('product_name'))
                            space.product.labelNewPrice.setText(Language.get('product_price'))
                            space.product.createProductButton.setText(Language.get("create"))
                            space.product.deleteProduct.setText(Language.get('del_product'))
                            space.product.editProduct.setText(Language.get('edit_product'))
                            space.product.editProductButton.setText(Language.get("save"))
                            space.product.addProduct.setText(Language.get("add_product"))
                            space.product.labelProduct.setText(Language.get('product'))
                            space.product.labelAmount.setText(Language.get('amount'))
            
            self.WINDOW.reOpenHome()
        except:
            self.WINDOW.setWindowTitle(Language.get("log_in"))
            self.WINDOW.log_in_title.setText(Language.get("log_in"))
            self.WINDOW.user_label.setText(Language.get("user_name"))
            self.WINDOW.password_label.setText(Language.get("password"))
            self.WINDOW.register_title.setText(Language.get("register"))
            self.WINDOW.access_offline_button.setText(Language.get("access_offline"))
            self.WINDOW.repeat_password_label.setText(Language.get("repeat_password"))
            self.WINDOW.password_input.setPlaceholderText(Language.get("enter_password"))
            self.WINDOW.user_name_input.setPlaceholderText(Language.get("enter_user_name"))
            self.WINDOW.repeat_password_input.setPlaceholderText(Language.get("enter_password"))

            if self.WINDOW.log_in:
                self.WINDOW.register_button.setText(Language.get("register"))
                self.WINDOW.log_in_button.setText(Language.get("log_in"))
            else:
                self.WINDOW.log_in_button.setText(Language.get("register"))
                self.WINDOW.register_button.setText(Language.get("log_in"))
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x, y):
        self.changer.move(x, y)

    def setGeometry(self, x, y, width, height):
        self.changer.setGeometry(x, y, width, height)

    def set_current_text(self, item):
        self.changer.setCurrentText(item)
