import os
from random import random
from tkinter import END

from pygame import mixer

from Player.song import Song


class Playlist:
    def __init__(self):
        self.songs = []
    #     self.playlist_files_folder = os.path.join(os.getcwd(), "playlist_files")
    #
    # def load_playlist(self, playlist_name):
    #     playlist_file_path = os.path.join(self.playlist_files_folder, f"{playlist_name}.txt")


    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def shuffle(self):
        random.shuffle(self.songs)

    def repeat(self):
        self.songs *= 2

    def volume(self, volume):
        mixer.music.set_volume(float(volume) / 100)

    # def load_directory(self, directory):
    #     self.clear()  # Clear the playlist
    #     self.directory = directory
    #     songs = []
    #     for file_name in os.listdir(directory):
    #         if file_name.endswith(".mp3"):
    #             song_path = os.path.join(directory, file_name)
    #             song = Song(song_path)
    #             songs.append(song)
    #             self.insert(END, song.title)
    #     self.songs = songs

