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
        self.main_window = window

    def init_ui(self, parent):
        self.changer = QComboBox(parent)
        self.changer.addItem("English")
        self.changer.addItem("Español")
        self.changer.addItem("Català")

        self.changer.setFont(FONT_SMALL_TEXT)
        self.changer.setGeometry(15, WINDOW_HEIGHT - 50, 100, 25)
        self.changer.setStyleSheet(COMBO_BOX)

    def init_events(self):
        self.changer.currentTextChanged.connect(self.change_lang)

    def change_lang(self, language: str):
        Language.change_language(language)

        self.language = language
        self.update_ui()

    def update_ui(self):
        try:
            self.main_window.storeNameInput.setPlaceholderText(Language.get("store") + str(len(STORES) + 1))
            self.main_window.createStoreButton.setText(Language.get("create_store"))
            self.main_window.editCategories.setText(Language.get("edit_categories"))
            self.main_window.setDefaultIcon.setText(Language.get("default_image"))
            self.main_window.icon_new_store.setText(Language.get("change_image"))
            self.main_window.storeNameLabel.setText(Language.get("name_store"))
            self.main_window.addStoreButton.setText(Language.get("add_store"))
            self.main_window.addShelfButton.setText(Language.get("add_shelf"))
            self.main_window.setWindowTitle(Language.get("window_title"))
            self.main_window.goHome.setText(Language.get("go_back"))

            self.main_window.categoryManager.showSpace.setText(Language.get("go_back"))
            self.main_window.categoryManager.saveCategory.setText(Language.get("save"))
            self.main_window.categoryManager.add_category_button.setText(Language.get("add_category"))
            self.main_window.categoryManager.categoryColor.setText(Language.get("select_color"))
            self.main_window.categoryManager.createCategoryButton.setText(Language.get("create"))
            self.main_window.categoryManager.cancelButtonAddCategory.setText(Language.get("cancel"))
            self.main_window.categoryManager.categoryNameLabel.setText(Language.get("category_name"))
            self.main_window.categoryManager.addCategoryName.setPlaceholderText(Language.get("name"))
            self.main_window.categoryManager.categoryColorLabel.setText(Language.get("category_color"))
            self.main_window.categoryManager.newCategoryColorButton.setText(Language.get("select_color"))
            
            # Shelf forms
            for shelfIndex, shelf in enumerate(SHELVES_FORMS):
                shelf.shelfLabel.setText(Language.get("shelf") + str(shelfIndex + 1))
                shelf.inputSpacesLabel.setText(Language.get("shelf_question_1"))
                shelf.doubleShelfLabel.setText(Language.get("shelf_question_2"))
                shelf.shelfFloorsLabel.setText(Language.get("shelf_question_4"))
                shelf.double_shelf_input.set_true_text(Language.get("yes"))
                shelf.double_shelf_input.set_false_text(Language.get("no"))

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
                        space.category_can_hold_product.set_true_text(Language.get("yes"))
                        space.category_can_hold_product.set_false_text(Language.get("no"))
                        space.openSpaceConfig.setText(Language.get("go_back"))
                        space.labelCategory.setText(Language.get("category"))

                        space.category.showSpace.setText(Language.get("go_back"))
                        space.category.saveCategory.setText(Language.get("save"))
                        space.category.add_category_button.setText(Language.get("add_category"))
                        space.category.categoryColor.setText(Language.get("select_color"))
                        space.category.createCategoryButton.setText(Language.get("create"))
                        space.category.cancelButtonAddCategory.setText(Language.get("cancel"))
                        space.category.categoryNameLabel.setText(Language.get("category_name"))
                        space.category.addCategoryName.setPlaceholderText(Language.get("name"))
                        space.category.categoryColorLabel.setText(Language.get("category_color"))
                        space.category.newCategoryColorButton.setText(Language.get("select_color"))

                        if isinstance(space.product, Product):
                            space.product.label_edit_product_name.setText(Language.get('edit_product_name'))
                            space.product.edit_product_name.setPlaceholderText(Language.get("product"))
                            space.product.edit_new_name.setPlaceholderText(Language.get("product"))
                            space.product.cancel_button_edit_product.setText(Language.get("cancel"))
                            space.product.label_new_product.setText(Language.get('product_name'))
                            space.product.add_product_button.setText(Language.get("add_product"))
                            space.product.cancel_add_product_button.setText(Language.get("cancel"))
                            space.product.label_new_price.setText(Language.get('product_price'))
                            space.product.create_product_button.setText(Language.get("create"))
                            space.product.delete_product.setText(Language.get('del_product'))
                            space.product.edit_product.setText(Language.get('edit_product'))
                            space.product.edit_product_button.setText(Language.get("save"))
                            space.product.label_product.setText(Language.get('product'))
                            space.product.label_amount.setText(Language.get('amount'))
            
            self.main_window.reOpenHome()
        except:
            self.main_window.setWindowTitle(Language.get("log_in"))
            self.main_window.log_in_title.setText(Language.get("log_in"))
            self.main_window.user_label.setText(Language.get("user_name"))
            self.main_window.password_label.setText(Language.get("password"))
            self.main_window.register_title.setText(Language.get("register"))
            self.main_window.access_offline_button.setText(Language.get("access_offline"))
            self.main_window.repeat_password_label.setText(Language.get("repeat_password"))
            self.main_window.password_input.setPlaceholderText(Language.get("enter_password"))
            self.main_window.user_name_input.setPlaceholderText(Language.get("enter_user_name"))
            self.main_window.repeat_password_input.setPlaceholderText(Language.get("enter_password"))

            if self.main_window.log_in:
                self.main_window.register_button.setText(Language.get("register"))
                self.main_window.log_in_button.setText(Language.get("log_in"))
            else:
                self.main_window.log_in_button.setText(Language.get("register"))
                self.main_window.register_button.setText(Language.get("log_in"))
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x: int, y: int):
        self.changer.move(x, y)

    def setGeometry(self, x: int, y: int, width: int, height: int):
        self.changer.setGeometry(x, y, width, height)

    def set_current_text(self, item: str):
        self.changer.setCurrentText(item)
