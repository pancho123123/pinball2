import pygame, random
from random import randint
from pathlib import Path

WIDTH = 450
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
#GREEN = (0, 255, 0)
#RED = (255,0,0)
#BLUE = (0,0,255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball")
clock = pygame.time.Clock()
current_path = Path.cwd()
file_path = current_path / 'highscore.txt'

def draw_text1(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

class RightB(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/rightbumper1.png"),(100,100)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 230
		self.rect.y = 510
		
	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_d]:
			self.image = pygame.transform.scale(pygame.image.load("img/rightbumper2.png"),(100,100)).convert()
			self.image.set_colorkey(WHITE)
			self.rect.y = 450
		if not keystate[pygame.K_d]:
			self.image = pygame.transform.scale(pygame.image.load("img/rightbumper1.png"),(100,100)).convert()
			self.image.set_colorkey(WHITE)
			self.rect.y = 510
		
class LeftB(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/leftbumper1.png"),(100,100)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 120
		self.rect.y = 510
		
	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.image = pygame.transform.scale(pygame.image.load("img/leftbumper2.png"),(100,100)).convert()
			self.image.set_colorkey(WHITE)
			self.rect.y = 450
		if not keystate[pygame.K_a]:
			self.image = pygame.transform.scale(pygame.image.load("img/leftbumper1.png"),(100,100)).convert()
			self.image.set_colorkey(WHITE)
			self.rect.y = 510

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/Ball1.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 200
		self.rect.y = 50
		self.start_position = 200, 50
		self.speedy = 2
		self.speedx = 1
		self.jumping = False
		self.Y_GRAVITY = 1
		self.JUMP_HEIGHT = 35
		self.Y_VELOCITY = self.JUMP_HEIGHT
		self.speed = (((self.speedx)**2)+((self.speedy)**2))**(1/2)
		self.counter1 = False
		self.counter2 = False
		self.counter3 = False
		self.counter4 = False
    
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		self.speedy += 0.1
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_SPACE]:
			self.jumping = True

class Bumper(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/bumper1.png"),(50,50)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()

class Bumper1(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 200
		self.rect.y = 200
		
	def update(self):
		pass

class Bumper2(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 170
		self.rect.y = 250
		
	def update(self):
		pass
		
class Bumper3(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 230
		self.rect.y = 250

	def update(self):
		pass

class Borde1(pygame.sprite.Sprite):# vertical izquierda
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/borde.png"),(1,600)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class Borde2(pygame.sprite.Sprite):# vertical derecha
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/borde.png"),(1,600)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 450
		self.rect.y = 0

class Borde3(pygame.sprite.Sprite):# horizontal arriba
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/borde.png"),(450,1)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class Borde4(pygame.sprite.Sprite):#vertical entremedio
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/borde.png"),(1,450)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 380
		self.rect.y = 150

class Borde5(pygame.sprite.Sprite):# inf1
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/bordeinf1.png"),(125,125)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 400

class Borde6(pygame.sprite.Sprite):# inf2
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/bordeinf2.png"),(60,60)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 325
		self.rect.y = 475

class Curva(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame .transform.scale(pygame.image.load("img/curva.png"),(140,140)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 325
		self.rect.y = 70

def show_go_screen():
	
	screen.fill(BLACK)
	draw_text1(screen, "Pinball", 65, WIDTH // 2, HEIGHT // 4)
	draw_text1(screen, "-", 20, WIDTH // 2, HEIGHT // 2)
	draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 3/4)
	draw_text1(screen, "Created by: Francisco Carvajal", 10,  60, 625)
	
	
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

def get_high_score():
	with open(file_path,'r') as file:
		return file.read()

def show_game_over_screen():
	screen.fill(BLACK)
	if highest_score <= score:
		draw_text1(screen, "¡high score!", 60, WIDTH  // 2, HEIGHT * 1/4)
		draw_text1(screen, "score: "+str(score), 30, WIDTH // 2, HEIGHT // 2)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 4/5)
	else:
		draw_text1(screen, "score: "+str(score), 60, WIDTH // 2, HEIGHT * 1/3)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 2/3)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

### high score

try:
	highest_score = int(get_high_score())
except:
	highest_score = 0

# Cargar imagen de fondo
background = pygame.transform.scale(pygame.image.load("img/fond.png").convert(),(450,600))


game_over = False
running = True
start = True
while running:
	screen.fill(BLACK)
	if game_over:

		show_game_over_screen()

		game_over = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		bumper1_list = pygame.sprite.Group()
		bumper2_list = pygame.sprite.Group()
		bumper3_list = pygame.sprite.Group()
		left_list = pygame.sprite.Group() 
		right_list = pygame.sprite.Group() 
		borde_list1 = pygame.sprite.Group()
		borde_list2 = pygame.sprite.Group()

		rightb = RightB()
		leftb = LeftB()
		ball = Ball()
		all_sprites.add(rightb, leftb, ball)
		left_list.add(leftb)
		right_list.add(rightb)
		borde1 = Borde1()
		borde2 = Borde2()
		borde3 = Borde3()
		borde4 = Borde4()
		borde5 = Borde5()
		borde6 = Borde6()
		curva = Curva()
		all_sprites.add(borde1, borde2, borde3, borde4, borde5, borde6, curva)
		borde_list1.add(borde1, borde2, borde4, borde5, borde6, curva)
		borde_list2.add(borde3, borde5, borde6, curva)

		
		bumper1 = Bumper1()
		bumper2 = Bumper2()
		bumper3 = Bumper3()
			
		all_sprites.add(bumper1, bumper2, bumper3)
		bumper1_list.add(bumper1)
		bumper2_list.add(bumper2)
		bumper3_list.add(bumper3)

				
		score = 0

	if start:

		show_go_screen()

		start = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		bumper1_list = pygame.sprite.Group()
		bumper2_list = pygame.sprite.Group()
		bumper3_list = pygame.sprite.Group()
		left_list = pygame.sprite.Group() 
		right_list = pygame.sprite.Group()
		borde_list1 = pygame.sprite.Group()
		borde_list2 = pygame.sprite.Group()
		
		rightb = RightB()
		leftb = LeftB()
		ball = Ball()
		all_sprites.add(rightb, leftb, ball)
		left_list.add(leftb)
		right_list.add(rightb)
		borde1 = Borde1()
		borde2 = Borde2()
		borde3 = Borde3()
		borde4 = Borde4()
		borde5 = Borde5()
		borde6 = Borde6()
		curva = Curva()
		all_sprites.add(borde1, borde2, borde3, borde4, borde5, borde6, curva)
		borde_list1.add(borde1, borde2, borde4, borde5, borde6, curva)
		borde_list2.add(borde3, borde5, borde6, curva)
		
		bumper1 = Bumper1()
		bumper2 = Bumper2()
		bumper3 = Bumper3()
			
		all_sprites.add(bumper1, bumper2, bumper3)
		bumper1_list.add(bumper1)
		bumper2_list.add(bumper2)
		bumper3_list.add(bumper3)
			
		score = 0
		
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if ball.jumping:
		ball.rect.bottom -= ball.Y_VELOCITY
		ball.Y_VELOCITY -= ball.Y_GRAVITY
		if ball.Y_VELOCITY < - ball.JUMP_HEIGHT:
			ball.jumping = False
			ball.Y_VELOCITY = ball.JUMP_HEIGHT	

	if ball.speedx > 0:
		ball.counter1 = True
	if ball.speedx < 0:
		ball.counter2 = True
	if ball.speedy > 0:
		ball.counter3 = True
	if ball.speedy < 0:
		ball.counter4 = True
	
	all_sprites.update()

	# termino del juego por borde inferior
	if ball.rect.top > 601:
		game_over = True

	
	# Checar colisiones - ball - left
	hits = pygame.sprite.spritecollide(ball, left_list, False)
	for hit in hits:
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			ball.speedx = -ball.speedx
			ball.speedy -= 3
		
	# Checar colisiones - ball- right
	hits = pygame.sprite.spritecollide(ball, right_list, False)
	for hit in hits:
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_d]:
			ball.speedx = -ball.speedx
			ball.speedy -= 3

	# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper1_list, False)
	for hit in hits:
		#print(ball.speed)
		score += 80
		ball.speedx = -ball.speedx
		ball.speedy = -ball.speedy
		
	# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper2_list, False)
	for hit in hits:
		#print(ball.speed)
		score += 80
		ball.speedx = -ball.speedx
		ball.speedy = -ball.speedy
	
	# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper3_list, False)
	for hit in hits:
		#print(ball.speed)
		score += 80
		ball.speedx = -ball.speedx
		ball.speedy = -ball.speedy

	# Checar colisiones - ball - borde1 borde2
	hits = pygame.sprite.spritecollide(ball, borde_list1, False)
	for hit in hits:
		if ball.counter1:
			ball.speedx = -ball.speedx
			ball.counter1 = False
		if ball.counter2:
			ball.speedx = -ball.speedx
			ball.counter2 = False
		
	# Checar colisiones - ball - borde3
	hits = pygame.sprite.spritecollide(ball, borde_list2, False)
	for hit in hits:
		if ball.counter3:
			ball.speedy = -ball.speedy
			ball.counter3 = False
		if ball.counter4:
			ball.speedy = -ball.speedy
			ball.counter4 = False

	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	#Marcador
	
	draw_text1(screen, str(score), 25, WIDTH // 2, 10)
	
	pygame.display.flip()