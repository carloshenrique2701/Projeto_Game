import pygame as pg
from settings import *

class PauseMenu:

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font_large = pg.font.Font(None, 100)
        self.font_medium = pg.font.Font(None, 50)
        self.font_small = pg.font.Font(None, 30)
        
        # Opções do menu
        self.options = [
            {"text": "Continuar", "key": pg.K_1, "action": self.continue_game},
            {"text": "Voltar ao Menu", "key": pg.K_2, "action": self.return_to_menu}
        ]
        self.selected_option = 0
        
        # Aviso sobre pontuação
        self.warning_text = "ATENÇÃO: Ao voltar para o menu, sua pontuação atual NÃO será salva"
    
    def continue_game(self):
        """Continua o jogo"""
        self.game.paused = False
        self.game.total_paused_time += pg.time.get_ticks() - self.game.pause_start_time
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.get_rel()
        
    def return_to_menu(self):
        """Volta para o menu principal"""
        self.game.reset_to_menu()
    
    def handle_events(self, event):
        """Processa eventos do menu de pause"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.continue_game()
            elif event.key == pg.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pg.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pg.K_RETURN:
                self.options[self.selected_option]["action"]()
            else:
                # Verifica teclas de atalho (1, 2)
                for i, option in enumerate(self.options):
                    if event.key == option["key"]:
                        option["action"]()
                        break
    
    def draw(self):
        """Desenha o menu de pause"""

        #Captura o tempo para printar na tela
        if self.game.paused:
            self.game.frozen_time_text = self.game.get_elapsed_time()

        # Fundo semi-transparente
        s = pg.Surface((width, height), pg.SRCALPHA)
        s.fill((20, 20, 20, 200))
        self.screen.blit(s, (0, 0))
        
        # Título
        title = self.font_large.render("PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width//2, height//2 - 100))
        self.screen.blit(title, title_rect)
        
        # Tempo atual
        time_text = self.font_small.render(f"Tempo: {self.game.frozen_time_text}", 
                                         True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(width//2, height//2 - 30))
        self.screen.blit(time_text, time_rect)
        
        # Opções do menu
        for i, option in enumerate(self.options):
            color = (100, 255, 100) if i == self.selected_option else (255, 255, 255)
            text = self.font_medium.render(f"{i+1} - {option['text']}", True, color)
            text_rect = text.get_rect(center=(width//2, height//2 + 50 + i * 70))
            self.screen.blit(text, text_rect)
            
            # Destaque visual
            if i == self.selected_option:
                pg.draw.rect(self.screen, (100, 100, 255, 100), 
                           text_rect.inflate(30, 15), 2, border_radius=5)
        
        # Aviso
        warning = self.font_small.render(self.warning_text, True, (255, 100, 100))
        warning_rect = warning.get_rect(center=(width//2, height - 50))
        self.screen.blit(warning, warning_rect)