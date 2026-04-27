import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()

        self.music_folder = music_folder
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith('.wav')]
        self.current_track = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return

        track_path = os.path.join(self.music_folder, self.playlist[self.current_track])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No music"
        return self.playlist[self.current_track]