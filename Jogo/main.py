import pygame as pg 
import sys 
import asyncio  
from settings import * 
from map import *
from object_render import *
from raycasting import * 
from sprite_object import * 
from object_handler import *
from weapon import *
from sound import * 
from pathfinding import *
from menu import MainMenu
from player import *
from victory import *
from pause_menu import *


class Game:

    def __init__(self):
        pg.init()

        # Configurações iniciais da tela
        self.screen = pg.display.set_mode(res) 
        self.clock = pg.time.Clock() # Controle de FPS do pygame
        self.delta_time = 1

        #Atributo global_event para disparar um evento a cada 40ms(milisegundos)
        self.global_event = pg.USEREVENT + 0 #USEREVENT é um evento do pygame que dispara um evento a cada 40ms
        pg.time.set_timer(self.global_event, 40)

        # Configurações iniciais do mouse
        pg.mouse.set_visible(True)  # Visível no menu
        pg.event.set_grab(False)    # Mouse livre

        # Estado do jogo
        self.running = False
        self.paused = False

        self.player_max_health = player_max_health
        self.enemies = 200

        self.difficulty_settings = None  

        # Carrega o menu primeiro e depois o audio
        self.menu = MainMenu(self)
        self.sound = Sound(self)


        self.font = pg.font.SysFont('fonts/resto.ttf', 30, True)

    def start_game(self):
        """Chamado quando o jogador seleciona 'Iniciar Jogo'"""
        # Aplica as configurações de dificuldade ANTES de criar os objetos
        if self.difficulty_settings:
            self.player_max_health = self.difficulty_settings['health']
            self.enemies = self.difficulty_settings['enemies']
        
        self.new_game()
        self.running = True
        
        # Configurações do mouse
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        
    #iniciando o jogo e declarando as instancias
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)
        self.victory = Victory(self)
        self.pause_menu = PauseMenu(self)

        # Temporizador
        self.start_time = pg.time.get_ticks()
        self.total_paused_time = 0
        self.pause_start_time = 0
        self.frozen_time_text = "00:00"
        self.draw_timer()

        if self.paused:
            self.pause_menu.draw()

    #Desenha o jogo, se estiver pausado, chama a tela de pause
    def draw(self):
        # Renderização normal do jogo
        self.object_renderer.draw()
        self.weapon.draw()
        
        # Sobrepõe a tela de pause se necessário
        if self.paused:
            self.pause_menu.draw() 
        elif hasattr(self, 'victory') and self.victory.show_victory:
            self.victory.draw()

    #Checa os eventos que são pegos a cada 40ms
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and self.running:
                    self.toggle_pause()
                elif self.paused:  # Só processa estas teclas se estiver pausado
                    self.pause_menu.handle_events(event)
                elif event.key == INTERACTION_KEY:
                    if self.player.check_puzzle_interaction():
                        print("Item coletado!")
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
            
    def toggle_pause(self):
        """Alterna entre pausado e despausado"""
        if not self.running:
            return
        
        if not self.paused:
            # Pausa o jogo
            self.paused = True
            self.frozen_time_text = self.get_elapsed_time()
            self.pause_start_time = pg.time.get_ticks()
            pg.mouse.set_visible(True)
            pg.event.set_grab(False)
            pg.mouse.set_pos([half_width, half_height])
            
            # Reseta estados de input
            self.player.shot = False
            pg.mouse.get_rel()  # Limpa movimento acumulado do mouse
        else:
            # Despausa o jogo
            self.paused = False
            self.total_paused_time += pg.time.get_ticks() - self.pause_start_time
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)
            
            # Garante que o próximo movimento do mouse não cause um salto
            pg.mouse.get_rel()

    def get_elapsed_time(self):
        if self.paused:
            return self.frozen_time_text
            
        current_time = pg.time.get_ticks()
        adjusted_time = current_time - self.start_time - self.total_paused_time
        total_seconds = adjusted_time // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"
    
    #Desenha o timer
    def draw_timer(self):
        # Atualiza o tempo congelado se estiver pausado
        if self.paused and not hasattr(self, 'last_paused_time'):
            self.frozen_time_text = self.get_elapsed_time()
        
        time_text = self.frozen_time_text if self.paused else self.get_elapsed_time()
        text_surface = self.font.render(f"Tempo: {time_text}", True, (255, 255, 255))
        self.screen.blit(text_surface, (width - 190, 10))

    def reset_to_menu(self):
        """Reseta o jogo e volta para o menu principal"""
        self.running = False
        self.paused = False
        self.player.points = 0
        self.player.health = 100
        self.menu = MainMenu(self)  # Recria o menu
        pg.mouse.set_visible(True)  # Mostra o cursor
        pg.event.set_grab(False)    # Libera o mouse

    #Basicamente vai funcionar como um loop de atualizações constantes do jogo
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        if hasattr(self, 'victory'):
            self.victory.update()

    #Principal loop do jogo - ASSÍNCRONO
    async def run(self): 
        while True:
            if not self.running:
                self.menu.handle_events()#chama o menu
                self.menu.draw()
            else:
                # Lógica normal do jogo
                self.check_events()    
                if not self.paused:
                    self.update()
                self.draw()

            pg.display.flip()#atualiza a tela
            self.delta_time = self.clock.tick(fps) # Controle de FPS
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}') # Mostra o FPS na tela
            
            # permite que o navegador processe outros eventos
            await asyncio.sleep(0)  

#executa o game com asyncio.run()
if __name__ == "__main__":
    game = Game() 
    asyncio.run(game.run()) 