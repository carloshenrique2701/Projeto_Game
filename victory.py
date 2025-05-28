import pygame as pg
from settings import *
import sys

class Victory:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_large = pg.font.Font(None, 120)
        self.font_small = pg.font.Font(None, 48)
        self.show_victory = False

    def end_game(self):
        #self.game.sound.victory.play()
        
        self.show_victory = True
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
        
        # Mostrar tela de vitória
        self.show_victory_screen()

        # Voltar ao menu principal
        self.game.reset_to_menu()


    def show_victory_screen(self):
        """Mostra a tela de vitória até o jogador pressionar ESC"""
        while True:
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
            instr_text = self.font_small.render("Pressione ESC para voltar ao menu", True, (100, 100, 100))
            instr_rect = instr_text.get_rect(center=(width//2, height//2 + 120))
            self.screen.blit(instr_text, instr_rect)
            
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # Fade out
                        fade = pg.Surface((width, height))
                        fade.fill((0, 0, 0))
                        for alpha in range(0, 300, 15):
                            fade.set_alpha(alpha)
                            self.screen.blit(fade, (0, 0))
                            pg.display.flip()
                            pg.time.delay(30)
                        return
                    
                