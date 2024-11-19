from app.styles.colorFunctions import get_contrast_color, darken_color, getStyleSheet

def test_get_contrast_color():
    assert get_contrast_color("#FFFFFF") == "#000000"
    assert get_contrast_color("#000000") == "#FFFFFF"

def test_darken_color():
    assert darken_color("#FFFFFF", 0.5) == "#7f7f7f"

def test_getStyleSheet():
    assert getStyleSheet("#FFFFFF") == """
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #b2b2b2;
            color: #000000;
        }
        QPushButton:hover {
            background-color: #f2f2f2;
            border: 1px solid #a5a5a5;
            color: #000000;
        }
        QPushButton:pressed {
            background-color: #e5e5e5;
            border: 1px solid #999999;
            color: #000000;
        }
    """