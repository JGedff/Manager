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
        self._language = 'English'
        self._main_window = window

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

        self._language = language
        self.update_ui()

    def update_ui(self):
        try:
            self._main_window.storeNameInput.setPlaceholderText(Language.get("store") + str(len(STORES) + 1))
            self._main_window.createStoreButton.setText(Language.get("create_store"))
            self._main_window.edit_categories_button.setText(Language.get("edit_categories"))
            self._main_window.setDefaultIcon.setText(Language.get("default_image"))
            self._main_window.icon_new_store.setText(Language.get("change_image"))
            self._main_window.storeNameLabel.setText(Language.get("name_store"))
            self._main_window.addStoreButton.setText(Language.get("add_store"))
            self._main_window.addShelfButton.setText(Language.get("add_shelf"))
            self._main_window.setWindowTitle(Language.get("window_title"))
            self._main_window.goHome.setText(Language.get("go_back"))

            self._main_window.categoryManager.stop_editting_category.setText(Language.get("go_back"))
            self._main_window.categoryManager.update_category_button.setText(Language.get("save"))
            self._main_window.categoryManager.add_category_button.setText(Language.get("add_category"))
            self._main_window.categoryManager.edit_category_color_selector.setText(Language.get("select_color"))
            self._main_window.categoryManager.create_category_button.setText(Language.get("create"))
            self._main_window.categoryManager.cancel_add_category_button.setText(Language.get("cancel"))
            self._main_window.categoryManager.label_input_edit_category_name.setText(Language.get("category_name"))
            self._main_window.categoryManager.input_new_category_name.setPlaceholderText(Language.get("name"))
            self._main_window.categoryManager.categoryColorLabel.setText(Language.get("category_color"))
            self._main_window.categoryManager.new_category_color_selector.setText(Language.get("select_color"))
            
            # Shelf forms
            for index, form in enumerate(SHELVES_FORMS):
                form.shelf_label.setText(Language.get("shelf") + str(index + 1))
                form.input_number_spaces_label.setText(Language.get("shelf_question_1"))
                form.input_double_shelf_label.setText(Language.get("shelf_question_2"))
                form.input_number_floors_label.setText(Language.get("shelf_question_4"))
                form.double_shelf_input.set_true_text(Language.get("yes"))
                form.double_shelf_input.set_false_text(Language.get("no"))

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
                        space.shelf_number.setText(Language.get("shelf") + str(space.shelf_i + 1) + ":")
                        space.label_can_hold_product.setText(Language.get("category_hold_product"))
                        space.category_can_hold_product.set_true_text(Language.get("yes"))
                        space.category_can_hold_product.set_false_text(Language.get("no"))
                        space.return_to_space_config.setText(Language.get("go_back"))
                        space.label_category_selected.setText(Language.get("category"))

                        space.category.stop_editting_category.setText(Language.get("go_back"))
                        space.category.update_category_button.setText(Language.get("save"))
                        space.category.add_category_button.setText(Language.get("add_category"))
                        space.category.edit_category_color_selector.setText(Language.get("select_color"))
                        space.category.create_category_button.setText(Language.get("create"))
                        space.category.cancel_add_category_button.setText(Language.get("cancel"))
                        space.category.label_input_edit_category_name.setText(Language.get("category_name"))
                        space.category.input_new_category_name.setPlaceholderText(Language.get("name"))
                        space.category.categoryColorLabel.setText(Language.get("category_color"))
                        space.category.new_category_color_selector.setText(Language.get("select_color"))

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
            
            self._main_window.reOpenHome()
        except:
            self._main_window.setWindowTitle(Language.get("log_in"))
            self._main_window.log_in_title.setText(Language.get("log_in"))
            self._main_window.user_label.setText(Language.get("user_name"))
            self._main_window.password_label.setText(Language.get("password"))
            self._main_window.register_title.setText(Language.get("register"))
            self._main_window.access_offline_button.setText(Language.get("access_offline"))
            self._main_window.repeat_password_label.setText(Language.get("repeat_password"))
            self._main_window.password_input.setPlaceholderText(Language.get("enter_password"))
            self._main_window.user_name_input.setPlaceholderText(Language.get("enter_user_name"))
            self._main_window.repeat_password_input.setPlaceholderText(Language.get("enter_password"))

            if self._main_window.log_in:
                self._main_window.register_button.setText(Language.get("register"))
                self._main_window.log_in_button.setText(Language.get("log_in"))
            else:
                self._main_window.log_in_button.setText(Language.get("register"))
                self._main_window.register_button.setText(Language.get("log_in"))

    def get_language(self):
        return self._language

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
