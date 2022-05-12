from json import loads, JSONDecodeError
import re
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem

from models.media_player import LMediaPlayer
from models.info_group import LInfoGroup
from models.history_group import LHistoryGroup
from models.control_group import LControlGroup
from models.stations_group import LStationsGroup

from functions.common_functions import download_icon


class MainWindow(QWidget):
    """ Main widget with resizable borders."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.resize(1024, 768)
        self.setWindowTitle("Radio Sub Stream")

        self.media_player = LMediaPlayer(self)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        stations_group = LStationsGroup(self, self.media_player)
        self.history_group = LHistoryGroup(self)

        top_layout = QHBoxLayout()
        top_layout.addWidget(stations_group)
        top_layout.addWidget(self.history_group)

        self.song_info_group = LInfoGroup(self)
        self.control_group = LControlGroup(self)

        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.song_info_group)
        self.main_layout.addWidget(self.control_group)

    def get_recent_tracks(self, sender_item):
        """ Displays song history for a selected radio station."""
        response = requests.get(sender_item.data(4))
        content = response.content.decode('utf-8', 'ignore')
        self.history_group.history_list.clear()
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
                    print(song)
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

            self.history_group.history_list.addItem(history_item)

    def get_song_data(self, sender_item):
        self.song_info_group.song_info_edit.clear()
        self.song_info_group.song_info_icon.setPixmap(QPixmap('fixtures/img/default_pixmap.ico'))
        if not sender_item:
            return
        if sender_item.data(5):
            unprocessed_name = f'{sender_item.data(3)}_{sender_item.data(4)}'.replace(' ', '_').replace('-', '_')
            icon_name = re.sub(r'\W', '', unprocessed_name)
            icon_path = download_icon(icon_url=sender_item.data(5), icon_name=icon_name)
            self.song_info_group.song_info_icon.setPixmap(QPixmap(icon_path))

        song_string = f'''
        name: {sender_item.data(3)}
        artist: {sender_item.data(4)}
        album name: {sender_item.data(6)}
        release year: {None}
        lyrics: {None}
        '''
        self.song_info_group.song_info_edit.append(song_string)

    def keyPressEvent(self, key_event):
        """ Checks all keyboard inputs, executes "MainWindow.switch_the_station()" if return key is pressed.
        param key_event: Keyboard key press event.
        type key_event: QKeyEvent
        """
        if key_event.key() == Qt.Key_Return:
            self.media_player.switch_the_station(self.media_player.stations_list.selectedItems()[0])
        else:
            super().keyPressEvent(key_event)
