def define_signals(main_window):
    main_window.media_player.stateChanged.connect(main_window.control_group.update_play_stop_button)
    main_window.media_player.stations_list.itemDoubleClicked.connect(main_window.media_player.switch_the_station)
    main_window.media_player.stations_list.currentItemChanged.connect(main_window.get_recent_tracks)
    main_window.control_group.volume_slider.valueChanged.connect(main_window.media_player.setVolume)
    main_window.history_group.history_list.currentItemChanged.connect(main_window.get_song_data)
