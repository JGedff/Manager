#### CLOSE MONGO CONNECTION SO ALL TESTS WORK PROPERLY ####
from app.utils.mongoDb import Mongo

if Mongo.connectionIsOpen():
    Mongo.closeMongoConnection()

#### GLOBAL VARIABLES FOR TESTING ####

from app.utils.category import Category
from app.utils.userManager import UserManager
from app.constants import STORES, SPACES, SHELVES, SHELVES_FORMS

from app.main import MainWindow, LogInWindow, Shelf

ARRAY_NUMBERS = []

class WINDOWS():
    mainWindow = None
    loginWindow = None

    @classmethod
    def start(cls):
        cls.mainWindow = MainWindow()
        cls.loginWindow = LogInWindow(cls.mainWindow)

    @classmethod
    def resetWindows(cls):
        Category.delAll()
        UserManager.username = ''
        UserManager.role = ''

        cls.mainWindow = MainWindow()
        cls.loginWindow = LogInWindow(cls.mainWindow)
    
    @staticmethod
    def resetGlobalVariables():
        STORES.clear()
        SPACES.clear()
        SHELVES.clear()
        SHELVES_FORMS.clear()

        Shelf.createShelf(None)
        Shelf.createShelf(None)

WINDOWS.start()