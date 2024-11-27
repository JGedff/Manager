import pytest

from PyQt5.QtCore import Qt

from app_tests.components.inputNumber import InputNumber

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def inputNumberOnlyButtons(qtbot):
    inputNumberObj = InputNumber()
    qtbot.addWidget(inputNumberObj)
    return inputNumberObj

@pytest.fixture
def inputNumberWriteNumber(qtbot):
    inputNumberObj = InputNumber(-5, True)
    qtbot.addWidget(inputNumberObj)
    return inputNumberObj

#### TESTS ####

def test_readOnlyInputButton(qtbot, inputNumberOnlyButtons):
    buttonAddNumber = inputNumberOnlyButtons.addNumber
    buttonRestNumber = inputNumberOnlyButtons.restNumber

    assert inputNumberOnlyButtons.inputNum.isReadOnly() == True
    assert inputNumberOnlyButtons.getNum() == 0

    qtbot.mouseClick(buttonAddNumber, Qt.LeftButton)

    assert inputNumberOnlyButtons.getNum() == 1

    qtbot.mouseClick(buttonRestNumber, Qt.LeftButton)

    assert inputNumberOnlyButtons.getNum() == 0

def test_inputButton(qtbot, inputNumberWriteNumber):
    buttonAddNumber = inputNumberWriteNumber.addNumber
    input = inputNumberWriteNumber.inputNum
    buttonRestNumber = inputNumberWriteNumber.restNumber

    assert input.isReadOnly() == False
    assert inputNumberWriteNumber.getNum() == -5

    qtbot.mouseClick(buttonAddNumber, Qt.LeftButton)

    assert inputNumberWriteNumber.getNum() == -4

    qtbot.mouseClick(buttonRestNumber, Qt.LeftButton)

    assert inputNumberWriteNumber.getNum() == -5

    # This lot of functions simulate someone deleting the - caracter before the number 5, and then, adding a 0 at the end
    # | => cursor of the input
    qtbot.mouseClick(input, Qt.LeftButton) # -5|
    qtbot.keyPress(input, Qt.Key_Left) # -|5
    qtbot.keyPress(input, Qt.Key_Backspace) # |5
    qtbot.keyPress(input, Qt.Key_Right) # 5|
    qtbot.keyClicks(input, "0") # 50|

    assert inputNumberWriteNumber.getNum() == 50

    qtbot.keyClicks(input, "A")

    assert inputNumberWriteNumber.getNum() == 50