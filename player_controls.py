from random import random
from random import shuffle

from tkinter import Button, Scale, HORIZONTAL, Listbox, Label, LabelFrame, filedialog, END, Scrollbar, VERTICAL, RIGHT, \
    BOTH, StringVar, LEFT, ACTIVE, Y, BOTTOM, X, ttk, DoubleVar
from tkinter import messagebox
import pygame.mixer as mixer
from song import Song
import os

class PlayerControls:
    def __init__(self, root, playlist):
        self.root = root
        self.playlist = playlist
        self.current_song = None
        self.is_playing = False
        self.is_shuffled = False
        self.is_repeated = False


        # Initializing the mixer
        mixer.init()


        # Create the necessary frames
        self.song_frame = LabelFrame(root, text='Current Song', bg='LightBlue', width=400, height=80)
        self.song_frame.place(x=0, y=0)

        self.button_frame = LabelFrame(root, text='Control Buttons', bg='Turquoise', width=400, height=200)
        self.button_frame.place(y=80)

        self.listbox_frame = LabelFrame(root, text='Playlist', bg='RoyalBlue')
        self.listbox_frame.place(x=400, y=0, height=200, width=300)

        # Create the necessary variables
        self.current_song = StringVar(root, value='<Not selected>')
        self.song_status = StringVar(root, value='<Not Available>')
        self.volume = DoubleVar(root, value=50)
        self.seek = DoubleVar(root, value=0)

        # Create the Playlist ListBox
        self.playlist = Listbox(self.listbox_frame, font=('Helvetica', 11), selectbackground='Gold')

        self.scroll_bar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.playlist.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.playlist.yview)

        self.scroll_bar.pack(side=RIGHT, fill=BOTH)
        self.playlist.pack(fill=BOTH, padx=5, pady=5)

        # Create the SongFrame Labels
        Label(self.song_frame, text='CURRENTLY PLAYING:', bg='LightBlue', font=('Times', 10, 'bold')).place(x=5, y=20)
        self.song_lbl = Label(self.song_frame, textvariable=self.current_song, bg='Goldenrod',
                               font=("Times", 12), width=25)
        self.song_lbl.place(x=150, y=20)

        # Create the Buttons in the main screen
        self.pause_btn = Button(self.button_frame, text='Pause', bg='Aqua', font=("Georgia", 13), width=7,
                                command=self.pause_song)
        self.pause_btn.place(x=15, y=55)

        self.stop_btn = Button(self.button_frame, text='Stop', bg='Aqua', font=("Georgia", 13), width=7,
                               command=self.stop_song)
        self.stop_btn.place(x=105, y=55)

        self.play_btn = Button(self.button_frame, text='Play', bg='Aqua', font=("Georgia", 13), width=7,
                               command=self.play_song)
        self.play_btn.place(x=195, y=55)

        self.resume_btn = Button(self.button_frame, text='Resume', bg='Aqua', font=("Georgia", 13), width=7,
                                 command=self.resume_song)
        self.resume_btn.place(x=285, y=55)

        self.load_btn = Button(self.button_frame, text='Load Directory', bg='Aqua', font=("Georgia", 13), width=35,
                               command=self.load_directory)
        self.load_btn.place(x=10, y=145)

        self.volume_slider = Scale(self.button_frame, from_=0, to=100, orient=HORIZONTAL, length=100, variable=self.volume, command=self.adjust_volume)
        self.volume_slider.set(50)  # Set initial volume level
        self.volume_slider.place(x=15, y=8)  # Adjust the coordinates as needed

        #
        self.seek_slider = Scale(self.button_frame, from_=0, to=100, orient=HORIZONTAL,
                                     length=150, variable=self.seek, command=self.seek_music)
        self.seek_slider.set(0.0)
        self.seek_slider.place(x=207, y=8)
        #
        self.shuffle_btn = Button(self.button_frame, text='Shuffle', background='Aqua', font=("Georgia", 13), width=7,
                                         command=self.toggle_shuffle)
        self.shuffle_btn.place(x=15, y=100)

        self.repeat_btn = Button(self.button_frame, text='Repeat', background='Aqua', font=("Georgia", 13), width=7,
                                        command=self.toggle_repeat)
        self.repeat_btn.place(x=285, y=100)

        # Create the progress bar
        self.progress_bar = ttk.Progressbar(root, mode='determinate')
        self.progress_bar.place(x=105, y=200, width=172, height= 30)

        # Set the progress bar initial value
        self.progress_bar["value"] = 0

        # Update the GUI
        self.root.update()

        # Label at the bottom that displays the state of the music
        Label(root, textvariable=self.song_status, bg='SteelBlue', font=('Times', 9), justify=LEFT).pack(side=BOTTOM, fill=X)

        # Finalize the GUI
        self.root.update()
        self.root.mainloop()

    def load_directory(self):
        directory = filedialog.askdirectory(title='Open a songs directory')
        if directory:
            self.directory = directory
            self.playlist.delete(0, END)  # Clear existing playlist
            songs = os.listdir(self.directory)
            self.playlist.insert(END, *songs)


    def play_song(self):
        song_name = self.playlist.get(ACTIVE)
        if song_name:
            song_path = os.path.join(self.directory, song_name)  # Get the full path of the song
            self.current_song.set(song_name)
            mixer.music.load(song_path)
            mixer.music.play()
            self.song_status.set("Song PLAYING")

    def stop_song(self):
        mixer.music.stop()
        self.song_status.set("Song STOPPED")

    def pause_song(self):
        mixer.music.pause()
        self.song_status.set("Song PAUSED")

    def resume_song(self):
        mixer.music.unpause()
        self.song_status.set("Song RESUMED")

    def adjust_volume(self, *args):
        volume = self.volume.get()
        mixer.music.set_volume(volume)

    def seek_music(self, position):
        position = float(position)  # Convert position to float
        current_time = mixer.music.get_pos() / 1000  # Get the current playback position in seconds

        # Get the total length of the song from the playlist
        song_name = self.playlist.get(ACTIVE)
        song = Song(song_name)
        total_length = song.get_length()

        desired_position = int(current_time + position)  # Calculate the desired position in seconds

        if desired_position > total_length:
            desired_position = total_length

        mixer.music.set_pos(desired_position)  # Seek to the desired position



    def toggle_shuffle(self):
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            self.shuffle_btn.config(text='Shuffle: On')
            playlist_items = list(self.playlist.get(0, 'end'))
            shuffle(playlist_items)
            self.playlist.delete(0, 'end')
            for item in playlist_items:
                self.playlist.insert('end', item)
        else:
            self.shuffle_btn.config(text='Shuffle: Off')
            self.playlist.delete(0, 'end')
            self.playlist.insert('end', *list(self.playlist.get(0, 'end')))

    def toggle_repeat(self):
        self.is_repeated = not self.is_repeated
        if self.is_repeated:
            self.repeat_btn.config(text='Repeat: On')
        else:
            self.repeat_btn.config(text='Repeat: Off')