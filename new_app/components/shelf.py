from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from styles.style_sheets import REST_BUTTON, BACKGROUND_BLACK
from styles.fonts import FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS

from utils.functions.shelf_functions import update_shelves_pos

from utils.language import Language

from components.input_bool import InputBool
from components.input_integer import InputInteger

class ShelfForm(QLabel):
    @staticmethod
    def create(parent: QWidget | None, main_window):
        length = len(SHELVES_FORMS)
        new_form = None

        if length > 0:
            new_form = ShelfForm(Language.get("shelf") + str(length + 1), SHELVES_FORMS[length - 1].pos().x(), SHELVES_FORMS[length - 1].pos().y() + 200, main_window, parent)
        else:
            new_form = ShelfForm(Language.get("shelf") + str(length + 1), 400, 300, main_window, parent)

        new_form.show()

        SHELVES_FORMS.append(new_form)

    @staticmethod
    def hide_all_forms(array_forms):
        for shelf in array_forms:
            shelf.hide()

    @staticmethod
    def show_all_forms(array_forms):    
        for shelf in array_forms:
            shelf.show()

    def __init__(self, name: str, posx: int, posy: int, main_window, parent: QWidget | None = None):
        super().__init__(parent)
        
        self.setGeometry(posx, posy, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.init_variables(main_window)
        self.init_ui(name)
        self.hide()

    def init_variables(self, main_window):
        self._main_window = main_window
        self._double_shelf = False
        self._spaces = 1
        self._floors = 1

    def init_ui(self, store_name: str):
        ## INITIALIZE OBJECTS ##
        # Labels
        self.shelf_label = QLabel(store_name, self)
        self.shelf_label.setGeometry(0, 10, 150, 35)

        self.input_number_spaces_label = QLabel(Language.get("shelf_question_1"), self)
        self.input_number_spaces_label.setGeometry(0, 55, 500, 35)

        self.input_double_shelf_label = QLabel(Language.get("shelf_question_2"), self)
        self.input_double_shelf_label.setGeometry(0, 95, 500, 35)

        self.input_number_floors_label = QLabel(Language.get("shelf_question_4"), self)
        self.input_number_floors_label.setGeometry(0, 135, 500, 35)

        # Inputs
        self.input_spaces = InputInteger(1, True, self)
        self.input_spaces.setGeometry(480, 35, 175, 65)

        self.input_shelf_floors = InputInteger(1, True, self)
        self.input_shelf_floors.setGeometry(480, 123, 175, 65)

        self.double_shelf_input = InputBool(Language.get("yes"), Language.get("no"), self)
        self.double_shelf_input.setGeometry(480, 92, 175, 34)

        # Style
        self.shelf_label.setFont(FONT_TEXT)
        self.input_double_shelf_label.setFont(FONT_SMALL_TEXT)
        self.input_number_spaces_label.setFont(FONT_SMALL_TEXT)
        self.input_number_floors_label.setFont(FONT_SMALL_TEXT)

        # Option to delete shelf if there is more than one shelf
        if len(SHELVES_FORMS) + 1 > 1:
            ## INITIALIZE OBJECTS ##
            # Labels
            # Horizontal line to separate forms
            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 650, 3)

            # Buttons
            self.delete_button = QPushButton("❌", self)
            self.delete_button.setGeometry(150, 15, 50, 25)

            ## STYLES ##
            # Labels
            self.separator.setStyleSheet(BACKGROUND_BLACK)

            # Buttons
            self.delete_button.setFont(FONT_SMALLEST_CHAR)
            self.delete_button.setStyleSheet(REST_BUTTON)

            # Set click event
            self.delete_button.clicked.connect(self.delete)

    def delete(self):
        index_to_delete = 0
        
        for index, form in enumerate(SHELVES_FORMS):
            try:
                if self.sender() == form.delete_button:
                    index_to_delete = index
                    break
            except AttributeError:
                continue
        
        SHELVES_FORMS[index_to_delete].hide()
        del SHELVES_FORMS[index_to_delete]

        update_shelves_pos(SHELVES_FORMS)
        self._main_window.resize_scroll_height()

    def save_info(self):
        self._spaces = self.input_spaces.get_value()
        self._floors = self.input_shelf_floors.get_value()
        self._double_shelf = self.double_shelf_input.get_value()

    def is_double_shelf(self):
        return self._double_shelf
    
    def get_num_spaces(self):
        return self._spaces

    def get_num_floors(self):
        return self._floors
