import pytest

from PyQt5.QtCore import Qt

from app.components.doubleButton import DoubleButton

from app.utils.functions.globalFunctions import useLessFunction

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def doubleButton(qtbot):
    doubleButton = DoubleButton("button1", "button2", add1, add20)
    qtbot.addWidget(doubleButton)
    return doubleButton

ARRAY_NUMBERS = []

def add1():
    ARRAY_NUMBERS.append(1)

def add20():
    ARRAY_NUMBERS.append(20)

#### TESTS ####

def test_subFunctionsWork(qtbot, doubleButton):
    assert ARRAY_NUMBERS == []

    qtbot.mouseClick(doubleButton.button1, Qt.LeftButton)

    assert ARRAY_NUMBERS == [1]

    qtbot.mouseClick(doubleButton.button2, Qt.LeftButton)

    assert ARRAY_NUMBERS == [1, 20]