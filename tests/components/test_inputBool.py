import pytest

from PyQt5.QtCore import Qt

from tests.functions.constantsForTest import ARRAY_NUMBERS
from tests.functions.functionsForTest import add1, add20

from app.components.inputBool import InputBool

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def useLessInputBoolean(qtbot):
    inputBooleanObj = InputBool("TRUE", "FALSE")
    qtbot.addWidget(inputBooleanObj)
    return inputBooleanObj

@pytest.fixture
def inputBoolean(qtbot):
    inputBooleanObj = InputBool("TRUE", "FALSE", None, add1, add20)
    qtbot.addWidget(inputBooleanObj)
    return inputBooleanObj

#### TESTS ####

def test_pressInputBoolean(qtbot, useLessInputBoolean):
    assert ARRAY_NUMBERS == [1, 20]

    assert useLessInputBoolean.getValue() == False

    qtbot.mouseClick(useLessInputBoolean.trueButton, Qt.LeftButton)

    assert useLessInputBoolean.getValue() == True

    qtbot.mouseClick(useLessInputBoolean.falseButton, Qt.LeftButton)

    assert useLessInputBoolean.getValue() == False

    assert ARRAY_NUMBERS == [1, 20]

def test_pressInputBooleanWithSubFunction(qtbot, inputBoolean):
    assert ARRAY_NUMBERS == [1, 20]

    qtbot.mouseClick(inputBoolean.falseButton, Qt.LeftButton)

    assert ARRAY_NUMBERS == [1, 20, 20]

    qtbot.mouseClick(inputBoolean.trueButton, Qt.LeftButton)
    
    assert ARRAY_NUMBERS == [1, 20, 20, 1]