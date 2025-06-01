from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        

        # spawn npc
        self.reward_NPC = False
        self.npc_positions = {}
        self.enemies = game.enemies if hasattr(game, 'enemies') else 100  # npc count
        print(f"\n \n \nenemies: {self.enemies} \n\n\n")
        print(f"\n \n \nhealth: {self.game.player.health} \n\n\n")
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()

        # sprite map
        add_sprite(AnimatedSprite(game))
        add_sprite(SpriteObject(game, pos=(17.5, 50)))
        add_sprite(SpriteObject(game, pos=(39.5, 48.5)))
        add_sprite(SpriteObject(game, pos=(15.5, 41.5)))
        add_sprite(SpriteObject(game, pos=(55.5, 49.5)))
        
        
    def spawn_npc(self):
        #spwana os npcs aleatoriamente pelo mapa
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_NPC(self):
        #Caso todos os inimigos sejam matados, o jogador ganha 5000 pontos
        if not len(self.npc_positions):
            self.game.player.points += 5000
            self.game.player.add_item_message(f"Parabéns, você matou todos os inimigos + 5000 pontos")
            self.reward_NPC = True

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        if not self.reward_NPC: self.check_NPC()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)