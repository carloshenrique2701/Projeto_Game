import pygame as pg
import sys
from settings import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        
        # Fontes
        self.font = pg.font.Font('resources/fonts/titulo.ttf', 74)
        self.small_font = pg.font.Font('resources/fonts/resto.ttf', 36)
        self.tips_font = pg.font.Font('resources/fonts/resto.ttf', 20)
        
        # Estados do menu
        self.state = "selecting_difficulty" # "selecting_difficulty", "confirming_start"
        self.difficulty_selected = None
        
        # Opções
        self.difficulty_options = ["Fácil", "Normal", "Expert", "Bruto", "Jiraya"]
        self.confirm_options = ["Iniciar Jogo", "Voltar"]
        self.selected = 0
        
        # Dicas de dificuldade
        self.difficulty_tips = {
            "Fácil": "Deixa de ser fraco seu vacilão, põe pelo menos no normal. FRANGO!",
            "Normal": "Você é um jogador normal que está em busca de novas experiências.",
            "Expert": "Você está se achando o melhor do mundo. Eu DUVIDO!",
            "Bruto": "De bruto tu não tem nada. Quando o teu fica na reta tu sai fora.",
            "Jiraya": "Tá se achando, não vai aguentar nem 15 segundos e vai ficar chorando depois."
        }
        
        # Configurações de dificuldade
        self.difficulty_settings = {
            "Fácil": {"enemies": 150, "health": 200},
            "Normal": {"enemies": 200, "health": 200},
            "Expert": {"enemies": 250, "health": 150},
            "Bruto": {"enemies": 300, "health": 150},
            "Jiraya": {"enemies": 350, "health": 100}
        }
    
    def draw(self):
        # Fundo escuro
        self.game.screen.fill((20, 20, 20))
        
        # Título
        title = self.font.render("Sussuros do Labirinto", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width//2, height//4))
        self.game.screen.blit(title, title_rect)
        
        if self.state == "selecting_difficulty":
            # Desenha opções de dificuldade
            for i, option in enumerate(self.difficulty_options):
                color = (255, 215, 0) if i == self.selected else (255, 255, 255)
                text = self.small_font.render(option, True, color)
                rect = text.get_rect(center=(width//2, height//2 + i*50))
                self.game.screen.blit(text, rect)
                
                # Mostra dica da dificuldade selecionada
                if i == self.selected:
                    tip = self.difficulty_tips[option]
                    help_text = self.tips_font.render(tip, True, (200, 200, 200))
                    help_rect = help_text.get_rect(center=(width//2, height - 50))
                    self.game.screen.blit(help_text, help_rect)
                    
        elif self.state == "confirming_start":
            # Desenha opções de confirmação
            for i, option in enumerate(self.confirm_options):
                color = (255, 215, 0) if i == self.selected else (255, 255, 255)
                text = self.small_font.render(option, True, color)
                rect = text.get_rect(center=(width//2, height//2 + i*50))
                self.game.screen.blit(text, rect)
                
            # Mostra dificuldade selecionada
            diff_text = self.small_font.render(f"Dificuldade: {self.difficulty_selected}", True, (200, 200, 200))
            diff_rect = diff_text.get_rect(center=(width//2, height//2 - 50))
            self.game.screen.blit(diff_text, diff_rect)
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    if self.state == "selecting_difficulty":
                        self.selected = (self.selected + 1) % len(self.difficulty_options)
                    else:
                        self.selected = (self.selected + 1) % len(self.confirm_options)
                elif event.key == pg.K_UP:
                    if self.state == "selecting_difficulty":
                        self.selected = (self.selected - 1) % len(self.difficulty_options)
                    else:
                        self.selected = (self.selected - 1) % len(self.confirm_options)
                elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    self.select_option()
                elif event.key == pg.K_ESCAPE and self.state == "confirming_start":
                    self.state = "selecting_difficulty"
                    self.selected = self.difficulty_options.index(self.difficulty_selected)

            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if self.state == "selecting_difficulty":
                    for i, option in enumerate(self.difficulty_options):
                        rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.selected = i
                else:
                    for i, option in enumerate(self.confirm_options):
                        rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.selected = i

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.check_mouse_click()
    
    def check_mouse_click(self):
        mouse_pos = pg.mouse.get_pos()
        
        if self.state == "selecting_difficulty":
            for i, _ in enumerate(self.difficulty_options):
                text_rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
                if text_rect.collidepoint(mouse_pos):
                    self.selected = i
                    self.select_option()
        else:
            for i, _ in enumerate(self.confirm_options):
                text_rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
                if text_rect.collidepoint(mouse_pos):
                    self.selected = i
                    self.select_option()
    
    def select_option(self):
        if self.state == "selecting_difficulty":
            # Apenas armazena a dificuldade selecionada
            self.difficulty_selected = self.difficulty_options[self.selected]
            self.state = "confirming_start"
            self.selected = 0  # Resetar seleção para "Iniciar Jogo"
            
        elif self.state == "confirming_start":
            if self.selected == 0:  
                # Aplica configurações da dificuldade
                settings = self.difficulty_settings[self.difficulty_selected]
                self.game.difficulty_settings = settings  # Armazena para usar depois
                
                # Inicia o jogo
                pg.mouse.get_rel()  # Reseta o mouse
                self.game.start_game()
                
            elif self.selected == 1:  # Voltar
                self.state = "selecting_difficulty"
                # Restaura a seleção anterior da dificuldade
                self.selected = self.difficulty_options.index(self.difficulty_selected)