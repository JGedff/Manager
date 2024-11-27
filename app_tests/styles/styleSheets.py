from app_tests.styles.colorFunctions import darken_color

INPUT_TEXT = f"""
    QLineEdit {{
        border: 1px solid #CACACA;
        padding-left: 5px;
    }}
    QLineEdit:hover {{
        border: 1px solid {darken_color("#CACACA", 0.7)};
    }}
"""

INPUT_NUMBER = f"""
    QLineEdit {{
        border: 1px solid #AFAFAF;
        padding-left: 5px;
    }}
    QLineEdit:hover {{
        border: 1px solid {darken_color("#AFAFAF", 0.7)};
    }}
"""

COMBO_BOX = f"""
    QComboBox {{
        border: 1px solid #AFAFAF;
        padding-left: 5px;
    }}
    QComboBox:hover {{
        border: 1px solid {darken_color("#AFAFAF", 0.7)};
    }}
"""

DEFAULT_BUTTON = f"""
    QPushButton {{
        background-color: #FFFFFF;
        border: 1px solid {darken_color("#FFFFFF", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #E6FDFF;
        border: 1px solid {darken_color("#E6FDFF", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#E6FDFF", 0.9)};
        border: 1px solid {darken_color("#E6FDFF", 0.6)}
    }}
"""

IMAGE_BUTTON = f"""
    QPushButton {{
        background-color: #FFFFFF;
        border: 1px solid {darken_color("#FFFFFF", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #DBFFD1;
        border: 1px solid {darken_color("#DBFFD1", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#DBFFD1", 0.9)};
        border: 1px solid {darken_color("#DBFFD1", 0.6)}
    }}
"""

IMPORTANT_ACTION_BUTTON = f"""
    QPushButton {{
        background-color: #59CC4E;
        border: 1px solid {darken_color("#59CC4E", 0.7)};
        color: white
    }}
    QPushButton:hover {{
        background-color: #43B538;
        border: 1px solid {darken_color("#43B538", 0.7)};
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#43B538", 0.9)};
        border: 1px solid {darken_color("#43B538", 0.6)};
    }}
    QPushButton:disabled {{
        background-color: #8DC987;
        border: 1px solid {darken_color("#8DC987", 0.7)};
    }}
"""

EDIT_BUTTON = f"""
    QPushButton {{
        background-color: #FFE397;
        border: 1px solid {darken_color("#FFE397", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #FAD778;
        border: 1px solid {darken_color("#FAD778", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#FAD778", 0.9)};
        border: 1px solid {darken_color("#FAD778", 0.6)}
    }}
"""

OFF_BUTTON = f"""
    QPushButton {{
        background-color: #DADADA;
        border: 1px solid {darken_color("#DADADA", 0.7)};
        color: #000000;
    }}
    QPushButton:hover {{
        background-color: #C4C4C4;
        border: 1px solid {darken_color("#C4C4C4", 0.7)};
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#C4C4C4", 0.9)};
        border: 1px solid {darken_color("#C4C4C4", 0.6)};
    }}
"""

REGISTER_BUTTON = f"""
    QPushButton {{
        background-color: #FFFFFF;
        border: 1px solid {darken_color("#FFFFFF", 0.7)};
    }}
    QPushButton:hover {{
        background-color: #E0FFF1;
        border: 1px solid {darken_color("#E0FFF1", 0.7)};
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#E0FFF1", 0.9)};
        border: 1px solid {darken_color("#E0FFF1", 0.6)};
    }}
"""

BLUE_BUTTON = f"""
    QPushButton {{
        background-color: #A4F9FF;
        border: 1px solid {darken_color("#A4F9FF", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #71E7f0;
        border: 1px solid {darken_color("#71E7f0", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#71E7f0", 0.9)};
        border: 1px solid {darken_color("#71E7f0", 0.6)}
    }}
    QPushButton:dsabled {{
        background-color: #C2FBFF;
        border: 1px solid {darken_color("#C2FBFF", 0.7)}
    }}
"""

ADD_BUTTON = f"""
    QPushButton {{
        background-color: #DBFFD1;
        border: 1px solid {darken_color("#DBFFD1", 0.7)};
    }}
    QPushButton:hover {{
        background-color: #B5FFA1;
        border: 1px solid {darken_color("#B5FFA1", 0.7)};
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#B5FFA1", 0.9)};
        border: 1px solid {darken_color("#B5FFA1", 0.6)};
    }}
"""

REST_BUTTON = f"""
    QPushButton {{
        background-color: #FFD1D6;
        border: 1px solid {darken_color("#FFD1D6", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #F7949F;
        border: 1px solid {darken_color("#F7949F", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#F7949F", 0.9)};
        border: 1px solid {darken_color("#F7949F", 0.6)}
    }}
    QPushButton:disabled {{
        background-color: #FFF2F2;
        border: 1px solid {darken_color("#FFF2F2", 0.7)}
    }}
"""

TRUE_BUTTON = f"""
    QPushButton {{
        background-color: #A4F9FF;
        border: 1px solid {darken_color("#A4F9FF", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #91EEFF;
        border: 1px solid {darken_color("#91EEFF", 0.7)};
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#91EEFF", 0.9)};
        border: 1px solid {darken_color("#91EEFF", 0.6)};
    }}
"""

FALSE_BUTTON = f"""
    QPushButton {{
        background-color: #FFFFFF;
        border: 1px solid {darken_color("#FFFFFF", 0.7)}
    }}
    QPushButton:hover {{
        background-color: #d4f7ff;
        border: 1px solid {darken_color("#d4f7ff", 0.7)}
    }}
    QPushButton:pressed {{
        background-color: {darken_color("#d4f7ff", 0.9)};
        border: 1px solid {darken_color("#d4f7ff", 0.6)}
    }}
"""

NO_RIGHT_BORDER_BUTTON_INPUT = """
    QLineEdit {
        border-right: 0px
    }
    QLineEdit:hover {
        border-right: 1px
    }
"""

NO_RIGHT_BORDER_BUTTON = """
    QPushButton {
        border-right: 0px
    }
    QPushButton:hover {
        border-right: 1px
    }
"""

BACKGROUND_BLACK = "background-color: #000000;"

BACKGROUND_GREY = "background-color: #DDDDDD;"