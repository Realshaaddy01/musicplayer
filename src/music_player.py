from tkinter import Tk
from playlist import Playlist
from player_controls import PlayerControls
from utils import load_songs_directory

# Creating the master GUI
root = Tk()
root.geometry('700x320')
root.title('Music Player From Python')
root.resizable(0, 0)

# Adding icon in window
root.iconbitmap('../Player/music-icon.png')



# Initialize the playlist
playlist = Playlist()

# Create player controls
controls = PlayerControls(root, playlist)

# Finalize the GUI
root.update()
root.mainloop()
