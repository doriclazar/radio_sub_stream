import sys
import json
import os
import requests
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSlider, QListWidget, QListWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

with open('data/radio_stations.json', 'r', encoding='utf-8') as radio_stations_file:
    radio_stations = json.loads(radio_stations_file.read())['radio_stations']

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.resize(800, 600)
        self.setWindowTitle("Radio Substream")

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        self.stations_list = QListWidget()

        radio_widgets = {}
        if not os.path.exists('data/icons'):
            os.makedirs('data/icons')
        for radio_station in radio_stations:
            icon_name = radio_station['name'].replace(' ', '-')
            icon_path = f'data/icons/{icon_name}.ico'
            if not os.path.exists(icon_path):
                icon_response = requests.get(radio_station['icon'])
                with open(icon_path, 'wb') as icon_file:
                    icon_file.write(icon_response.content)

            radio_widgets[radio_station['name']] = QListWidgetItem(radio_station['name'])

            radio_widgets[radio_station['name']].setData(3, radio_station['url'])
            radio_widgets[radio_station['name']].setIcon(QIcon(icon_path))
            self.stations_list.addItem(radio_widgets[radio_station['name']])

        self.stations_list.item(0).setSelected(True)
        self.stations_list.itemDoubleClicked.connect(self.switch_the_station)

        self.stations_list.currentItemChanged.connect(self.get_recent_tracks)
        main_layout.addWidget(self.stations_list, 0, 1)

        self.media_player = QMediaPlayer()
        self.media_player.setMedia(QMediaContent(QUrl(radio_stations[0]['url'])))

        self.media_player.stateChanged.connect(self.update_play_stop_button)

        volume_slider = QSlider(Qt.Vertical)
        volume_slider.setMaximum(100)
        volume_slider.valueChanged.connect(self.media_player.setVolume)
        volume_slider.setValue(15)

        main_layout.addWidget(volume_slider, 0, 0)

        self.play_stop_button = QPushButton("Play")
        self.play_stop_button.clicked.connect(self.play_stop)
        main_layout.addWidget(self.play_stop_button, 1, 1)

    def get_recent_tracks(self, sender_item):
        print(sender_item.data(3))

    def switch_the_station(self, sender_item):
        self.media_player.setMedia(QMediaContent(QUrl(sender_item.data(3))))
        self.media_player.play()

    def update_play_stop_button(self, is_playing):
        if is_playing:
            self.play_stop_button.setText('Stop')
        else:
            self.play_stop_button.setText('Play')

    def play_stop(self):
        if self.media_player.state():
            self.media_player.stop()
        else:
            self.media_player.play()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            # self.media_player.stop()
            self.switch_the_station(self.stations_list.selectedItems()[0])
        '''
        else:
            super().keyPressEvent(qKeyEvent)
        '''



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

