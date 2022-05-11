import json
import re
from json import loads, JSONDecodeError
import os
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import (QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
                             QSlider, QListWidget, QListWidgetItem, QGroupBox, QLabel)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from models.l_widgets import LSquareButton

with open('data/radio_stations.json', 'r', encoding='utf-8') as radio_stations_file:
    radio_stations = json.loads(radio_stations_file.read())['radio_stations']


class MainWindow(QWidget):
    """ Main widget with resizable borders."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.resize(1024, 768)
        self.setWindowTitle("Radio Sub Stream")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.stations_list = QListWidget()
        self.history_list = QListWidget()
        self._create_info_panel()

        self.media_player = QMediaPlayer()
        self.media_player.setMedia(QMediaContent(QUrl(radio_stations[0]['url'])))
        self.media_player.stateChanged.connect(self.update_play_stop_button)

        self.play_stop_button = LSquareButton('', self.play_stop, 'fixtures/img/play.png')
        self._create_control_panel()

    @staticmethod
    def download_icon(icon_url, icon_name):
        """ Downloads icon, and saves it to data path.
        param icon_url:
        param icon_name:
        return icon_path:
        """
        icon_path = f'data/icons/{icon_name}.ico'
        if os.path.exists(icon_path):
            return icon_path
        icon_response = requests.get(icon_url)
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon_response.content)
        return icon_path

    def _create_info_panel(self):
        """ Creates a panel with widgets for info display at the top of the main window."""

        # Stations list part
        stations_group = QGroupBox('Radio Stations')
        stations_layout = QHBoxLayout()
        radio_widgets = {}
        if not os.path.exists('data/icons'):
            os.makedirs('data/icons')
        for radio_station in radio_stations:
            station_name = radio_station['name']
            icon_name = station_name.replace(' ', '-')
            icon_path = self.download_icon(icon_url=radio_station['icon'], icon_name=icon_name)
            radio_widgets[station_name] = QListWidgetItem(station_name)
            radio_widgets[station_name].setData(3, radio_station['url'])
            radio_widgets[station_name].setData(4, radio_station['history_url'])
            radio_widgets[station_name].setData(5, radio_station['history_path'])
            radio_widgets[station_name].setIcon(QIcon(icon_path))
            self.stations_list.addItem(radio_widgets[station_name])
        self.stations_list.item(0).setSelected(True)
        self.stations_list.itemDoubleClicked.connect(self.switch_the_station)
        self.stations_list.currentItemChanged.connect(self.get_recent_tracks)
        stations_layout.addWidget(self.stations_list)
        stations_group.setLayout(stations_layout)

        # History part
        history_group = QGroupBox('Song History')
        history_layout = QHBoxLayout()
        self.history_list.currentItemChanged.connect(self.get_song_data)
        history_layout.addWidget(self.history_list)
        history_group.setLayout(history_layout)

        # Song info part
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
        song_info_group = QGroupBox('Song Details')
        song_info_group.setLayout(song_info_layout)

        # Top part
        top_layout = QHBoxLayout()
        top_layout.addWidget(stations_group)
        top_layout.addWidget(history_group)
        self.main_layout.addLayout(top_layout)

        self.main_layout.addWidget(song_info_group)

    def _create_control_panel(self):
        """ Creates a panel with widgets for control over radio stations at the bottom of the main window."""

        control_group = QGroupBox()
        control_group.setMaximumHeight(80)
        control_layout = QHBoxLayout()
        control_group.setLayout(control_layout)

        volume_slider = QSlider(Qt.Vertical)
        volume_slider.setMaximum(100)
        volume_slider.valueChanged.connect(self.media_player.setVolume)
        volume_slider.setValue(15)
        control_layout.addWidget(volume_slider)
        control_layout.addStretch(1)

        previous_play_button = LSquareButton('', self.previous_play, 'fixtures/img/step-backward.png')
        control_layout.addWidget(previous_play_button)

        previous_preview_button = LSquareButton('', self.previous_preview, 'fixtures/img/previous.png')
        control_layout.addWidget(previous_preview_button)

        control_layout.addWidget(self.play_stop_button)

        next_preview_button = LSquareButton('', self.next_preview, 'fixtures/img/next.png')
        control_layout.addWidget(next_preview_button)

        next_play_button = LSquareButton('', self.next_play, 'fixtures/img/step-forward.png')
        control_layout.addWidget(next_play_button)

        control_layout.addStretch(1)
        self.main_layout.addWidget(control_group)

    def previous_preview(self):
        """ Selects previous radio station."""
        current_row = self.stations_list.currentRow()
        if not current_row == 0:
            self.stations_list.setCurrentRow(current_row-1)

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

    def get_song_data(self, sender_item):
        self.song_info_edit.clear()
        self.song_info_icon.setPixmap(QPixmap('fixtures/img/default_pixmap.ico'))
        if not sender_item:
            return
        if sender_item.data(5):
            unprocessed_name = f'{sender_item.data(3)}_{sender_item.data(4)}'.replace(' ', '_').replace('-', '_')
            icon_name = re.sub(r'\W', '', unprocessed_name)
            icon_path = self.download_icon(icon_url=sender_item.data(5), icon_name=icon_name)

            self.song_info_icon.setPixmap(QPixmap(icon_path))

        song_string = f'''
        name: {sender_item.data(3)}
        artist: {sender_item.data(4)}
        album name: {sender_item.data(6)}
        release year: {None}
        lyrics: {None}
        '''
        self.song_info_edit.append(song_string)

    def get_recent_tracks(self, sender_item):
        """ Displays song history for a selected radio station."""

        response = requests.get(sender_item.data(4))
        content = response.content.decode('utf-8', 'ignore')
        self.history_list.clear()
        steps = sender_item.data(5).split(',')
        try:
            history = loads(content)
            for step in steps:
                history = history[step]
        except JSONDecodeError:
            history_xml = BeautifulSoup(content, 'html.parser')
            history = []
            try:
                for step_index in range(len(steps)):
                    if step_index < len(steps)-1:
                        history_xml = history_xml.find(f'{steps[step_index]}')
                    else:
                        history_xml = history_xml.find_all(f'{steps[step_index]}')

                for song in history_xml:
                    history.append({
                        'title': song.title.text,
                        'artist': song.artist.text,
                        'album': song.album.text,
                        'cover': song.albumart.text
                    })

            except Exception as e:
                print(type(e).__name__)
                print(e)
                return

        except Exception as e:
            print(type(e).__name__)
            print(e)
            return

        for song in history:
            history_item = QListWidgetItem()
            history_item.setText(f'{song["artist"]} - {song["title"]}')
            history_item.setData(3, song['artist'])
            history_item.setData(4, song['title'])

            # Add song icon if found in history
            existing_cover = song.get('cover')
            if not existing_cover:
                existing_cover = song.get('albumart')
            if existing_cover.replace(' ', ''):
                history_item.setData(5, existing_cover)

            # Add song album if found in history
            existing_album = song.get('album')
            if existing_album:
                if existing_album.replace(' ', ''):
                    history_item.setData(6, song['album'])

            self.history_list.addItem(history_item)

    def switch_the_station(self, sender_item):
        """ Plays selected radio station."""
        self.media_player.setMedia(QMediaContent(QUrl(sender_item.data(3))))
        self.media_player.play()

    def update_play_stop_button(self, is_playing):
        """ Switches "Stop" and "Play" signs for play_stop_button."""
        if is_playing:
            self.play_stop_button.setIcon(QIcon('fixtures/img/stop.png'))
        else:
            self.play_stop_button.setIcon(QIcon('fixtures/img/play.png'))

    def play_stop(self):
        """ Switches "Stop" and "Play" signs for play_stop_button."""
        if self.media_player.state():
            self.media_player.stop()
        else:
            self.switch_the_station(self.stations_list.selectedItems()[0])

    def keyPressEvent(self, key_event):
        """ Checks all keyboard inputs, executes "MainWindow.switch_the_station()" if return key is pressed.
        param key_event: Keyboard key press event.
        type key_event: QKeyEvent
        """
        if key_event.key() == Qt.Key_Return:
            self.switch_the_station(self.stations_list.selectedItems()[0])
        else:
            super().keyPressEvent(key_event)
