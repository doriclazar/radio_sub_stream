from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QPixmap


class LInfoGroup(QGroupBox):
    def __init__(self, parent=None):
        super(LInfoGroup, self).__init__(parent)
        self.setTitle('Song Details')

        self.song_info_icon = QLabel()
        self.song_info_icon.setMaximumSize(300, 300)
        self.song_info_icon.setScaledContents(True)
        self.song_info_icon.setPixmap(QPixmap('fixtures/img/default_pixmap.ico'))

        song_info_edit_font = QFont()
        song_info_edit_font.setPointSize(16)
        self.song_info_edit = QTextEdit()
        self.song_info_edit.setReadOnly(True)
        self.song_info_edit.setFont(song_info_edit_font)

        song_info_layout = QHBoxLayout()
        song_info_layout.addWidget(self.song_info_icon)
        song_info_layout.addWidget(self.song_info_edit)
        self.setLayout(song_info_layout)
