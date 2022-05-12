from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from PyQt5.QtWidgets import QListWidget


class LHistoryGroup(QGroupBox):
    def __init__(self, parent=None):
        super(LHistoryGroup, self).__init__(parent)
        self.setTitle('Song History')

        history_layout = QHBoxLayout()
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        self.setLayout(history_layout)
