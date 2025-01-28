import sys

from PyQt5.QtWidgets import QApplication

from utils.db import DB

from components.log_in import LogInWindow
from main import window


class app():
    application = QApplication(sys.argv)

    log_in_window = LogInWindow(window)
    log_in_window.show()

    sys.exit(application.exec_())

    DB.close_connection()

if __name__ == "__app__":
    app()
