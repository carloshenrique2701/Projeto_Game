from sprite_object import *


class Weapon(AnimatedSprite):

	# Inicializa um objeto Weapon com valores padrão para o caminho da imagem, escala e tempo de animação. 
	# Ele também configura a posição da arma, o estado de recarregamento e o valor de dano.
	def __init__(self, game, path='resources/sprites/weapon/0.png',scale=0.4, animation_time=90):
		super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
		self.images = deque(
			[pg.transform.smoothscale(img, (self.image.get_width() * scale,
				self.image.get_height() * scale))
			for img in self.images])
		self.weapon_pos = (half_width - self.images[0].get_width() // 2, height - self.images[0].get_height())
		self.reloading = False 
		self.num_images = len(self.images) #conta todas imagens da arma
		self.frame_counter = 0 
		self.damage = 50 #dano

	#Anima o tiro da arma rodando por uma sequência de imagens e atualizando o estado de recarregamento.
	def animate_shot(self):
		if self.game.paused: 
			return
		
		if self.reloading:
			self.game.player.shot = False 
			if self.animation_trigger:
				self.images.rotate(-1)
				self.image = self.images[0]
				self.frame_counter += 1 
				if self.frame_counter == self.num_images:
					self.reloading = False 
					self.frame_counter = 0

	def draw(self):
		#adiciona a primeira sprite da arma, na sua posição.
		self.game.screen.blit(self.images[0], self.weapon_pos)


	def update(self):
		if not self.game.paused:
			self.check_animation_time()
			self.animate_shot()
