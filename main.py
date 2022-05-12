import sys
from PyQt5.QtWidgets import QApplication
from models.main_window import MainWindow
from functions.signals import define_signals

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    define_signals(main_window)
    main_window.show()
    sys.exit(app.exec_())
