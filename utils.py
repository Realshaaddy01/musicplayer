import os
from tkinter import filedialog

from Player.song import Song


def load_songs_directory(playlist):
    songs_directory = filedialog.askdirectory(title='Open a songs directory')
    os.chdir(songs_directory)

    tracks = os.listdir()

    for track in tracks:
        song = Song(track)  # Assuming you have the Song class defined in song.py
        playlist.add_song(song)

# ... other utility functions ...
