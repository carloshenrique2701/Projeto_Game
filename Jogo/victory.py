import pygame as pg
from settings import *

class Victory:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_large = pg.font.Font(None, 120)
        self.font_small = pg.font.Font(None, 48)
        self.show_victory = False
        self.victory_start_time = 0

    def end_game(self):
        self.show_victory = True
        self.victory_start_time = pg.time.get_ticks()
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        pg.mouse.set_pos([half_width, half_height])
        
        # Reseta estados de input
        self.game.player.shot = False
        pg.mouse.get_rel()  # Limpa movimento acumulado do mouse
        
        # Calcular bônus de tempo
        time_str = self.game.get_elapsed_time()
        minutes = int(time_str.split(':')[0])
        
        if minutes <= 10:
            bonus = 4
        elif minutes <= 20:
            bonus = 3
        elif minutes <= 30:
            bonus = 2
        else:
            bonus = 1.5
            
        self.game.player.points = int(self.game.player.points * bonus)
        print("Pontuação = ", self.game.player.points)


    def update(self):
        if self.show_victory:
            current_time = pg.time.get_ticks()
            # Verifica se passaram 20 segundos ou se ESC foi pressionado
            if (current_time - self.victory_start_time > 15000) or self.check_escape_pressed():
                self.show_victory = False
                self.game.reset_to_menu()

    def check_escape_pressed(self):
        #se a tecla "g" for pressionada retorna True 
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_g:
                return True
        return False

    def draw(self):
        if self.show_victory:
            # Fundo branco
            self.screen.fill((255, 255, 255))
            
            # Texto "VICTORY"
            victory_text = self.font_large.render("VICTORY", True, (0, 0, 0))
            victory_rect = victory_text.get_rect(center=(width//2, height//2 - 50))
            self.screen.blit(victory_text, victory_rect)
            
            # Pontuação
            score_text = self.font_small.render(f"Pontuação Final: {self.game.player.points}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(width//2, height//2 + 50))
            self.screen.blit(score_text, score_rect)
            
            # Instruções
            instr_text = self.font_small.render("Pressione G para voltar ao menu", True, (100, 100, 100))
            instr_rect = instr_text.get_rect(center=(width//2, height//2 + 120))
            self.screen.blit(instr_text, instr_rect)