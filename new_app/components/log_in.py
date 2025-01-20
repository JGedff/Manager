from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from constants import STORES

from styles.style_sheets import INPUT_TEXT, OFF_BUTTON, REGISTER_BUTTON, IMPORTANT_ACTION_BUTTON
from styles.fonts import FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_BOLD_TITLE

from utils.user_manager import UserManager
from utils.language import Language
from utils.category import Category
from utils.mongoDb import Mongo

from utils.functions.space_category_functions import create_category_in, update_category_buttons_pos

from components.language_changer import LanguageChanger

class LogInWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()

        self.init_variables(main_app)
        self.init_ui(self.widget)
        self.init_events()

        self.setCentralWidget(self.scroll)

    def init_variables(self, main_app):
        # Properties
        self.logged = ""
        self.log_in = True
        self.main_app = main_app

        # Information
        self.setWindowTitle(Language.get("log_in"))
        self.setFixedSize(395, 605)

        # Display
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(390, 600)
        self.scroll.setWidget(self.widget)
    
    def init_ui(self, parent):
        ## INITIALIZE OBJECTS ##
        # Titles
        self.log_in_title = QLabel(Language.get("log_in"), parent)
        self.log_in_title.setGeometry(85, 55, 225, 50)
        
        self.register_title = QLabel(Language.get("register"), parent)
        self.register_title.setGeometry(85, 55, 225, 50)
        self.register_title.hide()

        # Labels
        self.user_label = QLabel(Language.get("user_name"), parent)
        self.user_label.setGeometry(15, 120, 200, 25)

        self.password_label = QLabel(Language.get("password"), parent)
        self.password_label.setGeometry(15, 220, 200, 25)

        self.repeat_password_label = QLabel(Language.get("repeat_password"), parent)
        self.repeat_password_label.setGeometry(15, 325, 340, 25)
        self.repeat_password_label.hide()

        # Buttons
        self.log_in_button = QPushButton(Language.get("log_in"), parent)
        self.log_in_button.setGeometry(15, 490, 355, 50)

        self.register_button = QPushButton(Language.get("register"), parent)
        self.register_button.setGeometry(270, 555, 100, 30)

        self.access_offline_button = QPushButton(Language.get("access_offline"), parent)
        self.access_offline_button.setGeometry(15, 555, 150, 30)

        # Inputs
        self.user_name_input = QLineEdit(parent)
        self.user_name_input.setGeometry(15, 150, 355, 50)
        self.user_name_input.setPlaceholderText(Language.get("enter_user_name"))

        self.password_input = QLineEdit(parent)
        self.password_input.setGeometry(15, 250, 355, 50)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(Language.get("enter_password"))

        self.repeat_password_input = QLineEdit(parent)
        self.repeat_password_input.setGeometry(15, 355, 355, 50)
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input.setPlaceholderText(Language.get("enter_password"))
        self.repeat_password_input.hide()

        # Others
        self.language_changer = LanguageChanger(self, parent)
        self.language_changer.setGeometry(265, 15, 100, 30)
        
        ## STYLES ##
        # Titles
        self.log_in_title.setFont(FONT_BOLD_TITLE)
        self.log_in_title.setAlignment(Qt.AlignCenter)

        self.register_title.setFont(FONT_BOLD_TITLE)
        self.register_title.setAlignment(Qt.AlignCenter)

        # Labels
        self.user_label.setFont(FONT_TEXT)
        self.password_label.setFont(FONT_TEXT)
        self.repeat_password_label.setFont(FONT_TEXT)

        # Buttons
        self.log_in_button.setFont(FONT_BIG_TEXT)
        self.log_in_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)

        self.register_button.setFont(FONT_SMALL_TEXT)
        self.register_button.setStyleSheet(REGISTER_BUTTON)

        self.access_offline_button.setFont(FONT_SMALL_TEXT)
        self.access_offline_button.setStyleSheet(OFF_BUTTON)

        # Inputs
        self.password_input.setFont(FONT_SMALL_TEXT)
        self.password_input.setStyleSheet(INPUT_TEXT)

        self.user_name_input.setFont(FONT_SMALL_TEXT)
        self.user_name_input.setStyleSheet(INPUT_TEXT)

        self.repeat_password_input.setFont(FONT_SMALL_TEXT)
        self.repeat_password_input.setStyleSheet(INPUT_TEXT)


    def init_events(self):
        # Clicking buttons
        self.log_in_button.clicked.connect(self.check_logging)
        self.register_button.clicked.connect(self.change_register_form)
        self.access_offline_button.clicked.connect(self.open_offline_version)

    def check_logging(self):
        authenticated = UserManager.authenticate(self.user_name_input.text(), self.password_input.text())

        if authenticated == 'NoInternet':
            self.access_offline()
        elif authenticated != None:
            self.logged_successful(self.user_name_input.text())
        else:
            self.logged_unsuccessful()

    def access_offline(self):
        # Manage user and role
        if UserManager.username != 'Guest' and UserManager.role != 'Offline':
            QMessageBox.information(self, "You don't have internet connection", "There was an issue with the network")
        else:
            QMessageBox.information(self, "Offline version", "You opened the offline version")

        self.main_app.change_user_role('Offline')

        UserManager.set_user('Guest', 'Offline')

        # Manage categories
        Category.add_category('Empty', 'white')
        Category.add_category('Unreachable', 'red')
        Category.add_category('Fill', 'green')
        Category.change_can_hold_product('Fill', True)

        create_category_in(self.main_app.shortcut_category, 'Empty', self.main_app.widget)
        create_category_in(self.main_app.shortcut_category, 'Unreachable', self.main_app.widget)
        create_category_in(self.main_app.shortcut_category, 'Fill', self.main_app.widget)
        update_category_buttons_pos(self.main_app.shortcut_category)

        # Manage language
        self.main_app.language_changer.change_lang(self.language_changer.language)
        self.main_app.language_changer.set_current_text(self.language_changer.language)
        self.main_app.language_changer.update()

        # Close log in window
        self.close()

        # Open main window
        self.main_app.store_name_input.setPlaceholderText(Language.get("store") + str(len(STORES) + 1))
        self.main_app.re_open_home()
        self.main_app.show()

    def logged_successful(self, username):
        # Manage user and role
        [_, role] = UserManager.findUser(username)
        UserManager.set_user(username, role)

        if UserManager.username == 'Guest' and UserManager.role == 'Offline':
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.information(None, "You don't have internet connection", "There was an issue with the network")

        else:
            QMessageBox.information(None, "Login successful", "Login successful")

        self.main_app.change_user_role(role, username)

        # Manage language
        self.main_app.language_changer.change_lang(self.language_changer.language)
        self.main_app.language_changer.set_current_text(self.language_changer.language)
        self.main_app.language_changer.update()

        # Download db information
        Mongo.get_mongo_info(self.main_app.widget, self.main_app.shortcut_category)

        # Close log in window
        self.close()

        # Open main window
        self.main_app.store_name_input.setPlaceholderText(Language.get("store") + str(len(STORES) + 1))
        self.main_app.re_open_home()
        self.main_app.show()
    
    def logged_unsuccessful(self):
        QMessageBox.warning(None, "Login Failed", "Incorrect username or password")

    def change_register_form(self):
        self.log_in = not self.log_in

        # Disconnect the function that executed when pressing from the button
        self.log_in_button.clicked.disconnect()

        if self.log_in: # Change ui to show the log in
            # Change title
            self.register_title.hide()
            self.log_in_title.show()

            # Change button names and styles
            self.log_in_button.setText(Language.get("log_in"))
            self.register_button.setText(Language.get("register"))

            self.log_in_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)
            self.register_button.setStyleSheet(REGISTER_BUTTON)

            # Hide repeat password input and label
            self.repeat_password_label.hide()
            self.repeat_password_input.hide()

            # Add a new function to be executed when pressing the button
            self.log_in_button.clicked.connect(self.check_logging)

        else: # Change ui to show the register
            # Change title
            self.log_in_title.hide()
            self.register_title.show()

            # Change button names and styles
            self.log_in_button.setText(Language.get("register"))
            self.register_button.setText(Language.get("log_in"))

            self.register_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)
            self.log_in_button.setStyleSheet(REGISTER_BUTTON)

            # Show repeat password input and label
            self.repeat_password_label.show()
            self.repeat_password_input.show()

            # Add a new function to be executed when pressing the button
            self.log_in_button.clicked.connect(self.register)

    def open_offline_version(self):
        UserManager.set_user('Guest', 'Offline')
        self.access_offline()

    def register(self):
        # Check buisness rules for name and password
        if len(self.user_name_input.text()) < 4:
            QMessageBox.warning(None, "Username too short", "The username must be at least 5 characters long")
        elif len(self.password_input.text()) < 8 or len(self.repeat_password_input.text().strip()) < 8:
            QMessageBox.warning(None, "Weak password", "The passwords must be 8 digits long")
        elif self.password_input.text() != self.repeat_password_input.text():
            QMessageBox.warning(None, "Diferent passwords", "The passwords must be the same")
        else:
            # Register
            registred = UserManager.register(self.user_name_input.text(), self.password_input.text())

            # Log in into the new user
            if registred == 'NoInternet':
                self.access_offline()
            elif registred == 'Duplicated':
                QMessageBox.warning(None, "Error: Duplicated", "The user already exists")
            elif registred != None:
                self.logged_successful(self.user_name_input.text())
            else:
                QMessageBox.warning(None, "Error: Unknown", "Try again later")
