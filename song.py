from mutagen.mp3 import MP3


class Song:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_length(self):
        audio = MP3(self.file_path)
        length_in_seconds = audio.info.length
        return length_in_seconds