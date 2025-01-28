import sys

from utils.db import DB

from components.log_in import LogInWindow
from main import application, window

class app():
    log_in_window = LogInWindow(window)
    log_in_window.show()

    sys.exit(application.exec_())

    DB.close_connection()

if __name__ == "__app__":
    app()
