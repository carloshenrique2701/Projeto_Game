import pygame as pg 
import os

class Sound:
    def __init__(self, game):
        self.game = game 
        pg.mixer.init()
        self.path = 'resources/sound/'
        
        # Sound effects
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        
        # Music playlist system
        self.themes_path = self.path + 'themes/'
        self.theme_files = sorted([f for f in os.listdir(self.themes_path) 
                                if f.endswith('.mp3')])
        self.current_theme_index = 0
        self.setup_music()
        
    def setup_music(self):
        if not self.theme_files:
            return
            
        pg.mixer.music.load(os.path.join(self.themes_path, self.theme_files[self.current_theme_index]))
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_endevent(pg.USEREVENT)
        
    def check_music_event(self, event):
        if event.type == pg.USEREVENT:
            self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_files)
            self.setup_music()