import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav'); self.shotgun.set_volume(0.2)
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav'); self.npc_pain.set_volume(0.2)
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav'); self.npc_death.set_volume(0.2)
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav'); self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav'); self.player_pain.set_volume(0.2)
        self.theme = pg.mixer.music.load(self.path + 'themes/0.mp3'); pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1)