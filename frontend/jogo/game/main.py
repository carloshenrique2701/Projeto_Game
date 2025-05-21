import pygame as pg 
import sys 
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

		# Carrega o menu primeiro
		self.menu = MainMenu(self)

		self.font = pg.font.SysFont('fonts/resto.ttf', 30, True)



	def start_game(self):
		"""Chamado quando o jogador seleciona 'Iniciar Jogo'"""
		self.new_game()
		self.running = True

		# Agora trava o mouse para gameplay e deixa ele invisível
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
		self.sound = Sound(self)
		self.pathfinding = PathFinding(self)

		#Temporizador
		self.start_time = pg.time.get_ticks()
		self.total_paused_time = 0
		self.pause_start_time = 0
		self.frozen_time_text = "00:00"

	#Desenha o jogo, se estiver pausado, chama a tela de pause
	def draw(self):
		# Renderização normal do jogo
		self.object_renderer.draw()
		self.weapon.draw()
		
		# Sobrepõe a tela de pause se necessário
		if self.paused:
			self.draw_pause_screen()

	#Desenha a tela de pause
	def draw_pause_screen(self):
		# Cria uma superfície semi-transparente
		s = pg.Surface((width, height), pg.SRCALPHA)
		s.fill((0, 0, 0, 180))
		self.screen.blit(s, (0, 0))
		
		# Texto de pause
		font = pg.font.Font(None, 100)
		text = font.render("PAUSED", True, (255, 255, 255))
		text_rect = text.get_rect(center=(width//2, height//2 - 50))
		self.screen.blit(text, text_rect)
		
		# Mostra o tempo congelado explicitamente
		time_surface = self.font.render(f"Tempo: {self.frozen_time_text}", True, (255, 255, 255))
		time_rect = time_surface.get_rect(center=(width//2, height//2 + 20))
		self.screen.blit(time_surface, time_rect)
		
		# Instruções
		font = pg.font.Font(None, 36)
		instructions = font.render("Pressione ESC to continue", True, (200, 200, 200))
		instructions_rect = instructions.get_rect(center=(width//2, height//2 + 50))
		self.screen.blit(instructions, instructions_rect)
	
	#Checa os eventos que são pegos a cada 40ms
	def check_events(self):
		self.global_trigger = False
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.toggle_pause()
				elif event.key == INTERACTION_KEY:
					if self.player.check_puzzle_interaction():
						print("Item coletado!")  # Log opcional
			elif event.type == self.global_event:
				self.global_trigger = True
			self.player.single_fire_event(event)

	def toggle_pause(self):
		if not self.running:
			return
			
		self.paused = not self.paused 
		pg.mouse.set_visible(self.paused)
		pg.event.set_grab(not self.paused)
		
		if self.paused:
			# Calcula o tempo REAL antes de pausar
			current_unpaused_time = pg.time.get_ticks() - self.start_time - self.total_paused_time
			total_seconds = current_unpaused_time // 1000
			minutes = total_seconds // 60
			seconds = total_seconds % 60
			self.frozen_time_text = f"{minutes:02}:{seconds:02}"
			
			self.pause_start_time = pg.time.get_ticks()
			pg.mouse.get_rel()
			pg.event.set_grab(False)
			pg.mouse.set_pos([half_width, half_height])
		else:
			self.total_paused_time += pg.time.get_ticks() - self.pause_start_time
			pg.mouse.get_rel()
			pg.event.set_grab(True)

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
		time_text = self.frozen_time_text if self.paused else self.get_elapsed_time()
		text_surface = self.font.render(f"Tempo: {time_text}", True, (255, 255, 255))
		self.screen.blit(text_surface, (width - 190, 10))  # canto superior direito



	#Basicamente vai funcionar como um loop de atualizações constantes do jogo
	def update(self):
		self.player.update()
		self.raycasting.update()
		self.object_handler.update()
		self.weapon.update()

	#Principal loop do jogo
	def run(self):
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

#executa o game
if __name__ == "__main__":
	game = Game() 
	game.run()
