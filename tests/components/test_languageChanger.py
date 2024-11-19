import pytest

from PyQt5.QtCore import Qt

from tests.functions.test_constantsForTest import LOGIN_WINDOW, MAIN_WINDOW

from app.components.languageChanger import LanguageChanger

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def mainLanguageChanger(qtbot):
    qComboBox = LanguageChanger(MAIN_WINDOW, MAIN_WINDOW.widget)
    qtbot.addWidget(qComboBox)
    return qComboBox

@pytest.fixture
def logInLanguageChanger(qtbot):
    qComboBox = LanguageChanger(LOGIN_WINDOW, LOGIN_WINDOW.widget)
    qtbot.addWidget(qComboBox)
    return qComboBox

#### TESTS ####

def test_changeMain(mainLanguageChanger):
    assert mainLanguageChanger.language == "English"
    assert MAIN_WINDOW.window().windowTitle() == "Manager"

    mainLanguageChanger.changeLang("Español")

    assert mainLanguageChanger.language == "Español"
    assert MAIN_WINDOW.window().windowTitle() == "Gestor"

    mainLanguageChanger.changeLang("Català")

    assert mainLanguageChanger.language == "Català"
    assert MAIN_WINDOW.window().windowTitle() == "Gestor"

    mainLanguageChanger.changeLang("English")

def test_changeLangLogIn(logInLanguageChanger):
    assert logInLanguageChanger.language == "English"
    assert LOGIN_WINDOW.window().windowTitle() == "Log in"

    logInLanguageChanger.changeLang("Español")

    assert logInLanguageChanger.language == "Español"
    assert LOGIN_WINDOW.window().windowTitle() == "Iniciar sesión"

    logInLanguageChanger.changeLang("Català")

    assert logInLanguageChanger.language == "Català"
    assert LOGIN_WINDOW.window().windowTitle() == "Iniciar sessió"

    logInLanguageChanger.changeLang("English")