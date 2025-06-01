import pygame as pg 
from settings import * 

class ObjectRenderer:

	def __init__(self, game):
		self.game = game 
		self.screen = game.screen
		self.wall_textures = self.load_wall_textures()

		#textura do ceu
		self.sky_image = self.get_texture('resources/textures/sky.png', (width, half_height))
		self.sky_offset = 0 

		#magem que indica que o player sofreu dano
		self.blood_screen = self.get_texture('resources/textures/blood_screen.png', res)

		#Texturas dos dígitos de sanidade / vida
		self.digit_size = 90 
		self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
							for i in range(11)]
		self.digits = dict(zip(map(str, range(11)), self.digit_images))
		self.game_over_image = self.get_texture('resources/textures/game_over.png', res)

		#Fonte do puzzle e points
		self.font = pg.font.SysFont('Arial', 16)
		self.points_font = pg.font.SysFont('Arial', POINTS_FONT_SIZE)

	def draw_puzzle_message(self):
		if self.game.player.near_puzzle_wall:
			text = self.font.render(INTERACTION_TEXT, True, PUZZLE_COLOR)
			text_rect = text.get_rect(center=(width - 800, height//2 - 50))
			self.screen.blit(text, text_rect)

	def draw_points(self):
		points_text = f"Pontos: {self.game.player.points}"
		text_surface = self.points_font.render(points_text, True, POINTS_COLOR)
		self.screen.blit(text_surface, POINTS_POSITION)	

	def draw_item_messages(self):
		"""Renderiza mensagens de itens no canto inferior esquerdo."""
		for i, msg in enumerate(self.game.player.item_messages):
			text = self.font.render(msg['text'], True, ITEM_MESSAGE_COLOR)
			text_rect = text.get_rect(center=(width - 800, height//2 + 100 + i * 50)) 
			self.screen.blit(text, text_rect)

	def draw_saved_item_messages(self):
		"""Renderiza mensagens de itens no canto inferior esquerdo."""
		for i, msg in enumerate(self.game.player.item_messages):
			text = self.font.render(msg['text'], True, SAVED_ITEM_MESSAGE)
			text_rect = text.get_rect(center=(width - 800, height//2 + 100 + i * 50)) 
			self.screen.blit(text, text_rect)

	def draw(self):
		self.draw_background()
		self.render_game_objects()
		self.draw_player_health()
		#Pequeno ponto branco da mira
		pg.draw.circle(self.screen, 'gray', (width / 2, (height/2) + 5), 5)
		self.game.draw_timer()
		self.draw_puzzle_message()
		self.draw_points()
		self.draw_item_messages()
		
	def game_over(self):		
		self.screen.blit(self.game_over_image, (0, 0)) #coloca a imagem de game over na tela 

	"""
	A lógica do laço é a seguinte:

	1- i recebe o índice da posição atual na string (começando em 0).
	2- char recebe o valor do caractere na posição atual (ou seja, o dígito da vida do jogador).
	3- O código usa o índice i para calcular a posição x na tela onde o dígito deve ser desenhado. A posição x é calculada multiplicando o índice i pelo tamanho do dígito (self.digit_size).
	4- O código desenha o dígito correspondente ao caractere char na posição calculada usando a função blit.
	5- O laço repete esses passos para cada caractere na string health.
	"""
	def draw_player_health(self):
		current_health = self.game.player.health
		# Calcula a porcentagem da vida atual em relação à vida máxima
		health_percentage = min(current_health / player_max_health, 1.0)  # Limita a 100% no máximo
		displayed_health = int(health_percentage * 100)  # Converte para valor entre 0-100
		
		health_str = str(displayed_health)
		for i, char in enumerate(health_str):
			self.screen.blit(self.digits[char], (i * self.digit_size, 0)) 
		self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))  # Mostra o símbolo de porcentagem 

	def player_damage(self):
		#sobrepõe a imagem do dano na tela se o player sofrer dano
		self.screen.blit(self.blood_screen, (0, 0))


	def draw_background(self):
		self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % width
		self.screen.blit(self.sky_image, (-self.sky_offset, 0))
		self.screen.blit(self.sky_image, (-self.sky_offset + width, 0))
		pg.draw.rect(self.screen, floor_color, (0, half_height, width, height))


	"""
	1- Ordenação dos objetos: A função sorted() é usada para ordenar a lista de objetos a serem renderizados (self.game.raycasting.objects_to_render) com base na profundidade (depth) 
	de cada objeto. A ordenação é feita em ordem decrescente (reverse=True), ou seja, os objetos mais distantes (com maior profundidade) são renderizados primeiro.
	
	2- Iteração sobre os objetos ordenados: A função for é usada para iterar sobre a lista ordenada de objetos. Cada objeto é representado por uma tupla (depth, image, pos) que contém:
	depth: a profundidade do objeto
	image: a imagem do objeto a ser renderizada
	pos: a posição do objeto na tela
	
	3- Renderização dos objetos: Para cada objeto, a função blit() é usada para renderizar a imagem do objeto na tela, na posição especificada (pos).
	"""
	def render_game_objects(self):
		list_objects = sorted(self.game.raycasting.objects_to_render ,\
			key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_objects:
			self.screen.blit(image, pos)


	@staticmethod #Metodo estatic para nao precisar instanciar a classe
	def get_texture(path, res=(texture_size, texture_size)):
		#carrega a imagem e converte para efeito alpha
		texture = pg.image.load(path).convert_alpha()
		#converte a resolução da imagem
		return pg.transform.scale(texture, res)


	#São usados numeros para referenciar as texturas nas paredes do minimap
	def load_wall_textures(self):
		return {
			1: self.get_texture('resources/textures/1.png'),
			2: self.get_texture('resources/textures/2.png'),
			3: self.get_texture('resources/textures/3.png'),
			4: self.get_texture('resources/textures/4.png'),
			5: self.get_texture('resources/textures/5.png'),
			6: self.get_texture('resources/textures/6.png'),
			7: self.get_texture('resources/textures/7.png'),
			9: self.get_texture('resources/textures/9.png'),
		}