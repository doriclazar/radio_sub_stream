from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QIcon

from models.square_button import LSquareButton


class LControlGroup(QGroupBox):
    def __init__(self, parent=None):
        super(LControlGroup, self).__init__(parent)

        self.setMaximumHeight(80)
        control_layout = QHBoxLayout()
        self.setLayout(control_layout)

        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(15)
        control_layout.addWidget(self.volume_slider)
        control_layout.addStretch(1)

        previous_play_button = LSquareButton(self, parent.media_player.previous_play, 'fixtures/img/step-backward.png')
        control_layout.addWidget(previous_play_button)

        previous_preview_button = LSquareButton(self, parent.media_player.previous_preview, 'fixtures/img/previous.png')
        control_layout.addWidget(previous_preview_button)

        self.play_stop_button = LSquareButton(self, parent.media_player.play_stop, 'fixtures/img/play.png')
        control_layout.addWidget(self.play_stop_button)

        next_preview_button = LSquareButton(self, parent.media_player.next_preview, 'fixtures/img/next.png')
        control_layout.addWidget(next_preview_button)

        next_play_button = LSquareButton(self, parent.media_player.next_play, 'fixtures/img/step-forward.png')
        control_layout.addWidget(next_play_button)

        control_layout.addStretch(1)

    def update_play_stop_button(self, is_playing):
        """ Switches "Stop" and "Play" signs for play_stop_button."""
        if is_playing:
            self.play_stop_button.setIcon(QIcon('fixtures/img/stop.png'))
        else:
            self.play_stop_button.setIcon(QIcon('fixtures/img/play.png'))
