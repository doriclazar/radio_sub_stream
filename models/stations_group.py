import os
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon
from functions.common_functions import download_icon


class LStationsGroup(QGroupBox):
    def __init__(self, parent=None, media_player=None):
        super(LStationsGroup, self).__init__(parent)
        self.setTitle('Radio Stations')

        stations_layout = QHBoxLayout()
        radio_widgets = {}
        if not os.path.exists('data/icons'):
            os.makedirs('data/icons')

        for radio_station in media_player.radio_stations:
            station_name = radio_station['name']
            icon_name = station_name.replace(' ', '-')
            icon_path = download_icon(icon_url=radio_station['icon'], icon_name=icon_name)
            radio_widgets[station_name] = QListWidgetItem(station_name)
            radio_widgets[station_name].setData(3, radio_station['url'])
            radio_widgets[station_name].setData(4, radio_station['history_url'])
            radio_widgets[station_name].setData(5, radio_station['history_path'])
            radio_widgets[station_name].setIcon(QIcon(icon_path))
            media_player.stations_list.addItem(radio_widgets[station_name])

        media_player.stations_list.item(0).setSelected(True)
        stations_layout.addWidget(media_player.stations_list)
        self.setLayout(stations_layout)
