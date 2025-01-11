import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from tests.functions.constantsForTest import WINDOWS

from app_tests.styles.styleSheets import IMPORTANT_ACTION_BUTTON, REGISTER_BUTTON
from app_tests.utils.mongoDb import Mongo

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def login_window(qtbot):
    window = WINDOWS.loginWindow
    qtbot.addWidget(window)
    return window

#### TESTS ####

def test_logInUnsuccessful(qtbot, login_window, monkeypatch):
    captured_title = None
    captured_message = None

    # Mock QMessageBox.exec_ to capture the QMessageBox instance
    def mock_exec(parent, title, text): # this parameters must have the same name as when the class / function is called
        nonlocal captured_title, captured_message

        captured_title = title
        captured_message = text

        return QMessageBox.Ok  # Simulate the "OK" button click

    # Replace QMessageBox.exec_ with the mock function
    monkeypatch.setattr(QMessageBox, "warning", mock_exec)

    # Simulate clicking the login button
    qtbot.mouseClick(login_window.logInButton, Qt.LeftButton)

    # Verify that the QMessageBox was shown
    assert captured_title == "Login Failed"
    assert captured_message == "Incorrect username or password"

def test_logInSuccessful(qtbot, login_window, monkeypatch):
    Mongo.reconnect()

    captured_title = None
    captured_message = None
    
    logInButton = login_window.logInButton
    inputUser = login_window.userQLineEdit
    inputPassword = login_window.passwordQLineEdit

    def mock_exec(parent, title, text):
        nonlocal captured_title, captured_message

        captured_title = title
        captured_message = text

        return QMessageBox.Ok

    monkeypatch.setattr(QMessageBox, "information", mock_exec)

    qtbot.mouseClick(inputUser, Qt.LeftButton)
    qtbot.keyClicks(inputUser, "jmmarmi")
    qtbot.mouseClick(inputPassword, Qt.LeftButton)
    qtbot.keyClicks(inputPassword, "12345678")
    qtbot.mouseClick(logInButton, Qt.LeftButton)

    assert captured_title == "Login successful"
    assert captured_message == "Login successful"

    Mongo.closeMongoConnection()

def test_accessOffline(qtbot, login_window, monkeypatch):
    captured_title = None
    captured_message = None
    
    offlineButton = login_window.accessOfflineButton

    def mock_exec(parent, title, text):
        nonlocal captured_title, captured_message

        captured_title = title
        captured_message = text

        return QMessageBox.Ok

    monkeypatch.setattr(QMessageBox, "information", mock_exec)

    qtbot.mouseClick(offlineButton, Qt.LeftButton)

    assert captured_title == "Offline version"
    assert captured_message == "You opened the offline version"

    WINDOWS.resetWindows()

def test_changeToRegister(qtbot, login_window):
    registerButton = login_window.registerButton
    loginButton = login_window.logInButton

    assert loginButton.text() == "Log in"
    assert loginButton.styleSheet() == IMPORTANT_ACTION_BUTTON
    
    assert registerButton.text() == "Register"
    assert registerButton.styleSheet() == REGISTER_BUTTON

    qtbot.mouseClick(registerButton, Qt.LeftButton)

    assert loginButton.text() == "Register"
    assert loginButton.styleSheet() == REGISTER_BUTTON

    assert registerButton.text() == "Log in"
    assert registerButton.styleSheet() == IMPORTANT_ACTION_BUTTON

    qtbot.mouseClick(registerButton, Qt.LeftButton)

def test_register(qtbot, login_window, monkeypatch):
    Mongo.reconnect()

    changeAction = login_window.registerButton
    doAction = login_window.logInButton

    username = login_window.userQLineEdit
    password = login_window.passwordQLineEdit
    repeatPassword = login_window.repeatPasswordQLineEdit

    captured_title = None
    captured_message = None

    def mock_exec(parent, title, text):
        nonlocal captured_title, captured_message

        captured_title = title
        captured_message = text

        return QMessageBox.Ok

    def mock_exec_info(parent, title, text):
        nonlocal captured_title, captured_message

        captured_title = title
        captured_message = text

        return QMessageBox.Ok

    monkeypatch.setattr(QMessageBox, "warning", mock_exec)
    monkeypatch.setattr(QMessageBox, "information", mock_exec_info)

    qtbot.mouseClick(changeAction, Qt.LeftButton)
    qtbot.mouseClick(doAction, Qt.LeftButton)

    assert captured_title == "Username too short"
    assert captured_message == "The username must be at least 5 characters long"

    qtbot.mouseClick(username, Qt.LeftButton)
    qtbot.keyClicks(username, "new15")

    qtbot.mouseClick(doAction, Qt.LeftButton)

    assert captured_title == "Weak password"
    assert captured_message == "The passwords must be 8 digits long"

    qtbot.mouseClick(password, Qt.LeftButton)
    qtbot.keyClicks(password, "12345678")

    qtbot.mouseClick(repeatPassword, Qt.LeftButton)
    qtbot.keyClicks(repeatPassword, "87654321")

    qtbot.mouseClick(doAction, Qt.LeftButton)

    assert captured_title == "Diferent passwords"
    assert captured_message == "The passwords must be the same"

    repeatPassword.setText("")

    qtbot.mouseClick(repeatPassword, Qt.LeftButton)
    qtbot.keyClicks(repeatPassword, "12345678")

    qtbot.mouseClick(doAction, Qt.LeftButton)

    assert captured_title == "Login successful"
    assert captured_message == "Login successful"

    Mongo.closeMongoConnection()
    WINDOWS.resetWindows()
