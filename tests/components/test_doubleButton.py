import pytest

from PyQt5.QtCore import Qt

from tests.functions.test_constantsForTest import ARRAY_NUMBERS
from tests.functions.test_functionsForTest import add1, add20

from app.components.doubleButton import DoubleButton

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def doubleButton(qtbot):
    doubleButton = DoubleButton("button1", "button2", add1, add20)
    qtbot.addWidget(doubleButton)
    return doubleButton

#### TESTS ####

def test_subFunctionsWork(qtbot, doubleButton):
    assert ARRAY_NUMBERS == []

    qtbot.mouseClick(doubleButton.button1, Qt.LeftButton)

    assert ARRAY_NUMBERS == [1]

    qtbot.mouseClick(doubleButton.button2, Qt.LeftButton)

    assert ARRAY_NUMBERS == [1, 20]