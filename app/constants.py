from PyQt5.QtGui import QFont

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 720

STORES = []
SPACES = [] # 2-dimension array
SHELVES = [] # 2-dimension array
SHELVES_FORMS = []

CATEGORY_NAMES = [] # ['Empty', 'Unreachable', 'Fill']
CATEGORY_COLORS = [] # ['white', 'red', 'green']

DEFAULT_SPACE_MARGIN = 75

DEFAULT_IMAGE = "img/magazine.png"

FONT_BOLD_TITLE = QFont()
FONT_BOLD_TITLE.setPointSize(24)

FONT_BIG_TEXT = QFont()
FONT_BIG_TEXT.setPointSize(16)

FONT_TEXT = QFont()
FONT_TEXT.setPointSize(14)

FONT_SMALL_TEXT = QFont()
FONT_SMALL_TEXT.setPointSize(12)

FONT_SMALL_BOLD_TEXT = QFont()
FONT_SMALL_BOLD_TEXT.setBold(True)
FONT_SMALL_BOLD_TEXT.setPointSize(12)

FONT_SMALLEST_CHAR = QFont()
FONT_SMALLEST_CHAR.setPointSize(11)