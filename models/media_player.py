import json
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class LMediaPlayer(QMediaPlayer):
    def __init__(self, parent=None):
        super(LMediaPlayer, self).__init__(parent)
        with open('data/radio_stations.json', 'r', encoding='utf-8') as radio_stations_file:
            self.radio_stations = json.loads(radio_stations_file.read())['radio_stations']

        self.setMedia(QMediaContent(QUrl(self.radio_stations[0]['url'])))
        self.stations_list = QListWidget()

    def previous_preview(self):
        """ Selects previous radio station."""
        current_row = self.stations_list.currentRow()
        if not current_row == 0:
            self.stations_list.setCurrentRow(current_row - 1)

    def previous_play(self):
        """ Selects previous radio station, and runs its stream."""
        self.previous_preview()
        self.switch_the_station(self.stations_list.selectedItems()[0])

    def next_preview(self):
        """ Selects next radio station."""
        current_row = self.stations_list.currentRow()
        if not current_row == self.stations_list.count() - 1:
            self.stations_list.setCurrentRow(current_row + 1)

    def next_play(self):
        """ Selects next radio station, and runs its stream."""
        self.next_preview()
        self.switch_the_station(self.stations_list.selectedItems()[0])

    def play_stop(self):
        """ Switches "Stop" and "Play" signs for play_stop_button."""
        if self.state():
            self.stop()
        else:
            self.switch_the_station(self.stations_list.selectedItems()[0])

    def switch_the_station(self, sender_item):
        """ Plays selected radio station."""
        self.setMedia(QMediaContent(QUrl(sender_item.data(3))))
        self.play()
