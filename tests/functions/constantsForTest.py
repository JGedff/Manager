#### CLOSE MONGO CONNECTION SO ALL TESTS WORK PROPERLY ####
from app.utils.mongoDb import Mongo

if Mongo.connectionIsOpen():
    Mongo.closeMongoConnection()

#### GLOBAL VARIABLES FOR TESTING ####

from app.utils.category import Category
from app.utils.userManager import UserManager

from app.main import MainWindow, LogInWindow

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

WINDOWS.start()
