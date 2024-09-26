WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 720

STORES = []
SHELVES = []

CATEGORY_NAMES = ['Empty', 'Unreachable', 'Fill']
CATEGORY_COLORS = ['white', 'red', 'green']
PRODUCT_CATEGORY = ['Fill']

DEFAULT_SHELF_PREFIX = "Shelf "
DEFAULT_SHELF_WIDTH = 400
DEFAULT_SHELF_HEIGHT = 130
DEFAULT_SHELF_MARGIN = 150

DEFAULT_SPACE_MARGIN = 75

DEFAULT_IMAGE = "img/magazine.png"

from utils.productInfo import ProductInfo

PRODUCTS_INFO = [ProductInfo(40258136797, "First product", 5.2, "2024/04/28", "MSelf"), ProductInfo(45, "Second product", 50, "2024/09/28", "MSelf")]