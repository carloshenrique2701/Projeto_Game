from settings import *
import pygame as pg 
import math 
from npc import * 
from object_handler import * 
import random
import asyncio

class Player:

	def __init__(self, game):

		self.game = game 
		self.x, self.y = player_pos
		self.angle = player_angle
		#se for True, significa que o jogador atirou.
		self.shot = False 

		#vida do player - 
		self.max_health = getattr(game, 'player_max_health', player_max_health)
		self.health = self.max_health
		if  self.max_health >= 250:
			self.health_recovery_delay = 1200 
		else:
			self.health_recovery_delay = 700
		self.time_prev = pg.time.get_ticks() #usado para calcular o atraso de recuperação de saúde
	
		#movimento do mouse
		self.rel = 0
		self.pitch = 0

		#puzzle
		self.near_puzzle_wall = False

		#pontos
		self.points = 0
		self.completed_events = set()
		self.item_messages = []
		self.last_message_time = 0

	"""
	Gerenciamento de Saúde

	recover_health: Recupera a saúde do jogador em 1 ponto se o atraso de recuperação de saúde tiver passado e a saúde do jogador for menor que a máxima.
	
	check_health_recovery_delay: Verifica se o atraso de recuperação de saúde tiver passado e retorna True se tiver.
	
	get_damage: Reduz a saúde do jogador por uma quantidade especificada e reproduz um efeito sonoro.
	"""
	#
	def recover_health(self):
		if self.check_health_recovery_delay() and self.health < self.max_health:
			self.health += 1 
	#
	def check_health_recovery_delay(self):
		time_now = pg.time.get_ticks()
		if time_now - self.time_prev > self.health_recovery_delay:
			self.time_prev = time_now
			return True 
	# 
	def get_damage(self, damage):
		#reduz a vida do player ao sofrer dano do inimigo
		self.health -= damage
		self.game.object_renderer.player_damage()
		self.game.sound.player_pain.play()

		#
		self.check_game_over()

	# Verifica se a saúde do jogador é menor que 1 e termina o jogo se for.
	def check_game_over(self):
		if self.health < 1:
			self.game.object_renderer.game_over()
			pg.display.flip()
			pg.time.delay(2500)
			self.game.pause_menu.return_to_menu()
			print("Pontuação = ", self.points)

	#verifica se o player pressionou o mouse para atirar
	def single_fire_event(self, event):
		if self.game.paused:
			return

		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1 and not self.shot and not self.game.weapon.reloading:
				self.game.sound.shotgun.play() #executa som de tiro ao atirar
				self.shot = True 
				self.game.weapon.reloading = True

	"""
	Movimento

	movement: Atualiza a posição do jogador com base na entrada do teclado e verifica colisões com paredes.

	check_wall: Verifica se uma posição dada é uma parede no mapa.

	check_wall_collision: Verifica colisões com paredes e atualiza a posição do jogador conforme necessário.
	"""
	#
	def movement(self):
		#movimento do player
		sin_a = math.sin(self.angle)
		cos_a = math.cos(self.angle)
		dx, dy = 0, 0
		speed = player_speed * self.game.delta_time
		speed_sin = speed * sin_a 
		speed_cos = speed * cos_a 

		#obtém e armazena todas as teclas pressionadas no game
		#dx e dy representam o deslocamento do player no mapa olhando de cima
		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			#vai para cima
			dx += speed_cos 
			dy += speed_sin
		if keys[pg.K_s]:
			#vai para baixo
			dx += -speed_cos
			dy += -speed_sin
		if keys[pg.K_a]:
			#vai para esquerda
			dx += speed_sin 
			dy += -speed_cos 
		if keys[pg.K_d]:
			#vai para direita
			dx += -speed_sin 
			dy += speed_cos


		#função que checa a colisão com as paredes do game
		self.check_wall_collision(dx, dy)
		self.angle %= math.tau #o angulo fica entre 0 e 2pi, evitando erros de arredondamento(overflow)
	#	
	def check_wall(self, x, y):
		return (x, y) not in self.game.map.world_map
	#
	def check_wall_collision(self, dx, dy):

		scale = player_size_scale / self.game.delta_time

		if self.check_wall(int(self.x + dx * scale), int(self.y)):
			self.x += dx 
		if self.check_wall(int(self.x), int(self.y + dy * scale)):
			self.y += dy

	#Atualiza o ângulo do jogador com base no movimento do mouse.
	def mouse_control(self):

		if self.game.paused:  # Só centraliza se o jogo não estiver pausado
			pg.mouse.get_rel()  # Descarta qualquer movimento durante o pause
			return

		mx, my = pg.mouse.get_rel()

		#movimento horizontal
		self.rel = mx
		self.angle += self.rel * mouse_sensitivity * self.game.delta_time
	
	
	def add_item_message(self, message):
		"""Adiciona uma mensagem temporária à lista."""
		self.item_messages.append({
			'text': message,
			'time': pg.time.get_ticks()
		})

	def update_messages(self):
		"""Remove mensagens expiradas."""
		current_time = pg.time.get_ticks()
		self.item_messages = [
			msg for msg in self.item_messages 
			if current_time - msg['time'] < ITEM_MESSAGE_DURATION
		]

	def check_puzzle_wall(self):
		self.near_puzzle_wall = False
		x, y = int(self.x), int(self.y)
		
		# Verifica paredes no raio de 2 blocos
		for i in range(x - PUZZLE_RADIUS, x + PUZZLE_RADIUS + 1):
			for j in range(y - PUZZLE_RADIUS, y + PUZZLE_RADIUS + 1):
				if (i, j) in self.game.map.world_map:
					wall_id = self.game.map.world_map[(i, j)]
					if wall_id in (5, 9):  # Verifica se é parede interativa (5 ou 9)
						# Verifica se o jogador está olhando para a parede
						ray_angle = self.angle
						dx = i + 0.5 - self.x
						dy = j + 0.5 - self.y
						distance = math.sqrt(dx ** 2 + dy ** 2)
						
						# Verifica se está dentro do campo de visão (FOV)
						target_angle = math.atan2(dy, dx)
						angle_diff = (target_angle - ray_angle + math.pi) % (2 * math.pi) - math.pi
						
						if abs(angle_diff) < half_fov and distance < PUZZLE_RADIUS + 1:
							self.near_puzzle_wall = True
							return

	def check_puzzle_interaction(self):
		"""Verifica interação com paredes id=5 ou 9"""
		x, y = int(self.x), int(self.y)
		for i in range(x - PUZZLE_RADIUS, x + PUZZLE_RADIUS + 1):
			for j in range(y - PUZZLE_RADIUS, y + PUZZLE_RADIUS + 1):
				if (i, j) in self.game.map.world_map:
					wall_id = self.game.map.world_map[(i, j)]
					if wall_id == 9:  # Parede de vitória
						self.game.victory.end_game()
						return True
					elif wall_id == 5:  # Parede de itens normais
						event_id = f"item_{i}_{j}_{wall_id}"
						if event_id not in self.completed_events:
							points = random.randint(45, 120)
							item_name = random.choice(ITEM_NAMES)
							self.add_points(points, event_id)
							self.add_item_message(f"{item_name} +{points} pontos")
							return True
						else:
							self.add_item_message(SAVED_ITEM_MESSAGE)
		return False

	def get_tile_in_front(self):
		# Calcula a posição à frente do jogador
		front_x = int(self.x + math.cos(self.angle) * 1.5)
		front_y = int(self.y + math.sin(self.angle) * 1.5)
		return (front_x, front_y)

	def add_points(self, amount, event_id=None):
		"""
		Adiciona pontos e registra o evento (se fornecido).
		- `amount`: Quantidade de pontos a adicionar.
		- `event_id`: Identificador único do puzzle/item (evita repetição).
		"""
		if event_id and event_id in self.completed_events:
			return  # Evento já foi contabilizado
		
		self.points += amount
		if event_id:
			self.completed_events.add(event_id)

	def add_npc_kill_points(self, npc_pos):
		"""Adiciona pontos aleatórios (78-220) por matar um NPC."""
		event_id = f"npc_kill_{npc_pos[0]}_{npc_pos[1]}"  # ID único baseado na posição do NPC
		if event_id not in self.completed_events:
			points = random.randint(78, 220)
			self.add_points(points, event_id)

	#atualiza o movimento do player constantemente para que ele consiga andar
	def update(self):
		self.movement()
		self.mouse_control()
		self.recover_health()
		self.check_puzzle_wall()
		self.update_messages()

	#Retorna a posição atual do player
	@property 
	def pos(self):
		return self.x, self.y 

	#Retorna a posição do jogador no mapa.
	@property
	def map_pos(self):
		return int(self.x), int(self.y)
	