import pytest

from PyQt5.QtCore import Qt

from tests.functions.constantsForTest import WINDOWS

from app.components.languageChanger import LanguageChanger

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def mainLanguageChanger(qtbot):
    qComboBox = LanguageChanger(WINDOWS.mainWindow, WINDOWS.mainWindow.widget)
    qtbot.addWidget(qComboBox)
    return qComboBox

@pytest.fixture
def logInLanguageChanger(qtbot):
    qComboBox = LanguageChanger(WINDOWS.loginWindow, WINDOWS.loginWindow.widget)
    qtbot.addWidget(qComboBox)
    return qComboBox

#### TESTS ####

def test_changeMain(mainLanguageChanger):
    assert mainLanguageChanger.language == "English"
    assert WINDOWS.mainWindow.window().windowTitle() == "Manager"

    mainLanguageChanger.changeLang("Español")

    assert mainLanguageChanger.language == "Español"
    assert WINDOWS.mainWindow.window().windowTitle() == "Gestor"

    mainLanguageChanger.changeLang("Català")

    assert mainLanguageChanger.language == "Català"
    assert WINDOWS.mainWindow.window().windowTitle() == "Gestor"

    mainLanguageChanger.changeLang("English")

def test_changeLangLogIn(logInLanguageChanger):
    assert logInLanguageChanger.language == "English"
    assert WINDOWS.loginWindow.window().windowTitle() == "Log in"

    logInLanguageChanger.changeLang("Español")

    assert logInLanguageChanger.language == "Español"
    assert WINDOWS.loginWindow.window().windowTitle() == "Iniciar sesión"

    logInLanguageChanger.changeLang("Català")

    assert logInLanguageChanger.language == "Català"
    assert WINDOWS.loginWindow.window().windowTitle() == "Iniciar sessió"

    logInLanguageChanger.changeLang("English")