import pygame as pg
from settings import *

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Fontes consistentes com o menu principal
        self.title_font = pg.font.Font('fonts/titulo.ttf', 74)
        self.main_font = pg.font.Font('fonts/resto.ttf', 36)
        self.small_font = pg.font.Font('fonts/resto.ttf', 24)
        
        # Opções do menu
        self.options = [
            {"text": "Continuar", "key": pg.K_1, "action": self.continue_game},
            {"text": "Voltar ao Menu", "key": pg.K_2, "action": self.return_to_menu}
        ]
        self.selected_option = 0
        
        # Aviso sobre pontuação
        self.warning_text = "ATENÇÃO: Ao voltar para o menu, sua pontuação atual NÃO será salva"
        
        # Cores consistentes com o menu principal
        self.title_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 215, 0)  # Dourado
        self.warning_color = (255, 100, 100)
        self.help_color = (200, 200, 200)
    
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
        # Captura o tempo para printar na tela
        if self.game.paused:
            self.game.frozen_time_text = self.game.get_elapsed_time()

        # Fundo semi-transparente (mais escuro que o menu principal)
        s = pg.Surface((width, height), pg.SRCALPHA)
        s.fill((10, 10, 10, 220))  # Quase preto com alta transparência
        self.screen.blit(s, (0, 0))
        
        # Título (menor que no menu principal)
        title = self.title_font.render("PAUSADO", True, self.title_color)
        title_rect = title.get_rect(center=(width//2, height//4))
        self.screen.blit(title, title_rect)
        
        # Opções do menu
        for i, option in enumerate(self.options):
            y_pos = height//2 + i * 60
            color = self.selected_color if i == self.selected_option else self.text_color
            
            # Texto da opção
            text = self.main_font.render(option["text"], True, color)
            text_rect = text.get_rect(center=(width//2, y_pos))
            self.screen.blit(text, text_rect)
            
            # Destaque visual para opção selecionada
            if i == self.selected_option:
                # Ícone de seleção (seta dourada)
                arrow = self.main_font.render(">", True, self.selected_color)
                self.screen.blit(arrow, (text_rect.left - 40, y_pos - text_rect.height//2))
                
                arrow = self.main_font.render("<", True, self.selected_color)
                self.screen.blit(arrow, (text_rect.right + 20, y_pos - text_rect.height//2))
        
        # Aviso (na parte inferior)
        warning = self.small_font.render(self.warning_text, True, self.warning_color)
        warning_rect = warning.get_rect(center=(width//2, height - 80))
        self.screen.blit(warning, warning_rect)
        
        # Instruções (consistentes com o menu principal)
        help_text = self.small_font.render("Use as setas UP e DOWN para navegar | ENTER para selecionar", 
                                         True, self.help_color)
        help_rect = help_text.get_rect(center=(width//2, height - 30))
        self.screen.blit(help_text, help_rect)