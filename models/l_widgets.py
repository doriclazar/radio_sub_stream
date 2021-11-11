from PyQt5.QtWidgets import QPushButton, QListWidget
from PyQt5.QtGui import QIcon


class LSquareButton(QPushButton):
    def __init__(self, parent=None, signal=None, icon_path=None):
        super(LSquareButton, self).__init__(parent)
        self.setMaximumHeight(60)
        self.setMinimumWidth(self.height())
        self.setMaximumWidth(self.height())
        self.setIcon(QIcon(icon_path))
        self.clicked.connect(signal)
