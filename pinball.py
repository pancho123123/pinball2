import pygame, random, math
from random import randint
from pathlib import Path
from abc import ABC, abstractmethod


WIDTH = 450
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
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

arc_rect = screen.get_rect().move(0,HEIGHT/2)
arc_center = arc_rect.center
arc_radio = min(arc_rect.size)/2
arc_start = math.pi/6 #30°
arc_stop = 2*math.pi/3 #120°

def direction(a,b):
	#x,y vector from a to b
	if hasattr(a,'rect'):
		xa = a.rect.centerx
		ya = a.rect.centery
	else:
		xa, ya = a
	if hasattr(b,'rect'):
		xb = b.rect.centerx
		yb = b.rect.centery
	else:
		xb, yb = b
	dx = xb -xa
	dy = yb - ya
	return dx, dy

def distance(a,b):
	#pitagoras distance between a and b
	dx, dy = direction(a,b)
	return (dx**2 + dy**2)**(1/2)

def reflection(normal, i_vector, impulse = 1):
	'i_vector reflection with normal vector.'
	if complex(*normal) != 0 and complex(*i_vector) != 0:
		alpha = complex(*normal) / abs(complex(*normal))
		incidence =complex(*i_vector) / abs(complex(*i_vector))
		rotated = -complex(*i_vector) * (alpha/incidence)**2
		rotated *= impulse
		reflected = rotated.real, rotated.imag
	else:
		reflected = i_vector
	return reflected

# Wall abstract base class, not intended tu instantiate.
# use the specific wall classes below
# CircunWall,
class Wall(ABC):

	@abstractmethod
	def draw(self, surface):
		pass

	@abstractmethod
	def collide(self, o):
		pass

	@abstractmethod
	def bounce(self, o):
		pass

	def move_to_safe(self, o):
		while self.collide(o):
			o.rect.x += o.speedx
			o.rect.y += o.speedy

class CircunWall(Wall):
	def __init__(self, center, radio, color):
		self.center = center
		self.radio = radio
		self.color = color

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.center, self.radio)

	def collide(self, o):
		centers_distance = distance(o.rect.center, self.center)
		distance_to_circunf = self.radio - centers_distance
		return -o.radio < distance_to_circunf < o.radio

	def bounce(self, o, impulse=None):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx , o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

class ArcWall(Wall):
	def __init__(self, center, radio, start, stop, color):
		self.center = center
		self.radio = radio
		diam = 2*radio
		self.rect = pygame.Rect(center, (diam, diam)).move(-radio, -radio)
		self.start = start
		self.stop = stop
		if self.stop < self.start:
			self.stop += math.tau
		self.color = color

	def draw(self, surface):
		pygame.draw.arc(surface, self.color, self.rect, -self.stop, -self.start )

	def collide(self, o):
		colliding = False
		o_rel_x, o_rel_y = direction(self.center, o)
		o_angle = math.atan2(o_rel_y, o_rel_x)
		if o_angle < 0:
			o_angle += math.tau
		if self.start <= o_angle <= self.stop:
			centers_distance = distance(o.rect.center, self.center)
			distance_to_circunf = self.radio - centers_distance
			colliding = -o.radio < distance_to_circunf < o.radio
		return colliding

	def bounce(self, o, impulse=None):
		normal = direction(self.center, o.rect.center)
		i_vector = o.speedx, o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

class LineWall(Wall):
	def __init__(self, start, stop, color):
		self.start = start
		self.stop = stop
		self.color = color

	def draw(self, surface):
		pygame.draw.line(surface, self.color, self.start, self.stop)

	def collide(self, o):
		p = complex(*direction(self.start, o.rect.center))
		ba = complex(*direction(self.start, self.stop))
		pba = p/ba
		if 0 <= pba.real <= 1:
			line_distance = abs(pba.imag*ba)
		else:
			line_distance = min(
				distance(self.start, o.rect.center), 
				distance(self.stop, o.rect.center))
		return line_distance < o.radio

	def bounce(self, o, impulse=None):
		normal = direction(self.start, self.stop)
		i_vector = -o.speedx, -o.speedy
		if impulse:
			o.speedx, o.speedy = reflection(normal, i_vector, impulse)
		else:
			o.speedx, o.speedy = reflection(normal, i_vector)

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
		self.image = pygame.image.load("img/Ball1.png").convert_alpha()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = screen.get_rect().center
		self.rect.x, self.rect.y = 400, 570
		self.start_position = 400, 570
		self.radio = self.rect.w/2
		self.speedy = 0
		self.speedx = 2
		self.jumping = False
		self.Y_GRAVITY = 1
		self.JUMP_HEIGHT = 35
		self.Y_VELOCITY = self.JUMP_HEIGHT
		self.counter1 = False
		self.counter2 = False
		self.counter3 = False
		self.counter4 = False

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		self.speedy += 0.1
		if self.speedy < 0:
			self.speedy += 0.005*abs(self.speedy)
		if self.speedy > 0:
			self.speedy -= 0.005*abs(self.speedy)
		if self.speedx < 0:
			self.speedx += 0.005*abs(self.speedx)
		if self.speedx > 0:
			self.speedx -= 0.005*abs(self.speedx)
		
		if self.rect.x < 0 or self.rect.x > 450:
			self.speedx = -self.speedx
		if self.rect.y < 0:
			self.speedy = -self.speedy
		
		
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_SPACE]:
			if self.rect.x > 390 and self.rect.y > 570:
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
		self.rect.y = 190
		
	def update(self):
		pass

class Bumper2(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 160
		self.rect.y = 260
		
	def update(self):
		pass
		
class Bumper3(Bumper):
	def __init__(self):
		super().__init__()
		self.rect.x = 240
		self.rect.y = 260

	def update(self):
		pass

class Borde1(pygame.sprite.Sprite):# vertical izquierda
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(1,600)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class Borde2(pygame.sprite.Sprite):# vertical derecha
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(1,600)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 450
		self.rect.y = 0

class Borde3(pygame.sprite.Sprite):# horizontal arriba
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(450,1)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class Borde4(pygame.sprite.Sprite):#vertical entremedio
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(1,450)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 380
		self.rect.y = 150

class Borde5(pygame.sprite.Sprite):# inf1
	def __init__(self):
		super().__init__()
		self.image =  pygame.transform.rotate(diagonal_izquierda, -45)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 400

class Borde6(pygame.sprite.Sprite):# diagonal inf derecha
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.rotate(diagonal_derecha, 45)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 325
		self.rect.y = 475

class Borde7(pygame.sprite.Sprite):# horizontal inf der
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(50,1)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 400
		self.rect.y = 600

class Borde8(pygame.sprite.Sprite):#vertical pequeño que cierra la partida
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/borde.png"),(1,100)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 390
		self.rect.y = 50

class Curva(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/curva.png"),(140,160)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = 310
		self.rect.y = 30

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

# Cargar imagenes
diagonal_derecha = pygame.transform.scale(pygame.image.load("img/borde.png"),(76,1))
diagonal_izquierda = pygame.transform.scale(pygame.image.load("img/borde.png"),(177,1))

background = pygame.transform.scale(pygame.image.load("img/fond.png").convert(),(450,600))


game_over = False
running = True
start = True

circle1 = CircunWall((225,215), 23, RED)
circle2 = CircunWall((185,285), 23, RED)
circle3 = CircunWall((265,285), 23, RED)
arc1 = ArcWall((350,150),100 , 270*math.pi/180, 5*math.pi/180  , RED)
arc2 = ArcWall((290,200),100 , 270*math.pi/180, 5*math.pi/180  , RED)
line1 = LineWall((0,404), (150,550), RED)
line2 = LineWall((300,550), (380,475), RED)
walls = [circle1, circle2, circle3, arc1, arc2, line1, line2]
counter = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			sys.exit()

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
		borde_list3 = pygame.sprite.Group()

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
		borde7 = Borde7()
		borde8 = Borde8()
		curva = Curva()
		all_sprites.add(borde1, borde2, borde3, borde4, borde5, borde6, borde7, borde8, curva)
		borde_list1.add(borde1, borde2, borde4, borde5, borde6, curva)
		borde_list2.add(borde3, borde5, borde6, borde7, curva)
		borde_list3.add(borde8)

		
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
		borde_list3 = pygame.sprite.Group()
		
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
		borde7 = Borde7()
		borde8 = Borde8()
		curva = Curva()
		all_sprites.add(borde1, borde2, borde3, borde4, borde5, borde6, borde7, borde8, curva)
		borde_list1.add(borde1, borde2, borde4, borde5, borde6, curva)
		borde_list2.add(borde3, borde5, borde6, borde7, curva)
		borde_list3.add(borde8)
		
		bumper1 = Bumper1()
		bumper2 = Bumper2()
		bumper3 = Bumper3()
			
		all_sprites.add(bumper1, bumper2, bumper3)
		bumper1_list.add(bumper1)
		bumper2_list.add(bumper2)
		bumper3_list.add(bumper3)
			
		score = 0
		

	for w in walls:
		w.draw(screen)
	
	clock.tick(60)
	
	

	if ball.jumping:
		ball.rect.bottom -= ball.Y_VELOCITY
		ball.Y_VELOCITY -= ball.Y_GRAVITY
		if ball.Y_VELOCITY < - ball.JUMP_HEIGHT:
			ball.jumping = False
			ball.Y_VELOCITY = ball.JUMP_HEIGHT	

	
	all_sprites.update()
	for w in walls:
		if w.collide(ball):
			if w is circle1 or circle2 or circle3:
				w.bounce(ball, impulse = 1.7)
				score += 80
			w.move_to_safe(ball)
			#if w in [circle1,circle2,circle3]:
						

	# termino del juego por borde inferior
	if ball.rect.top > 610:
		game_over = True

	
	# Checar colisiones - ball - left
	hits = pygame.sprite.spritecollide(ball, left_list, False)
	for hit in hits:
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			ball.speedx = -ball.speedx
			ball.speedy -= 2
		
	# Checar colisiones - ball- right
	hits = pygame.sprite.spritecollide(ball, right_list, False)
	for hit in hits:
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_d]:
			ball.speedx = -ball.speedx
			ball.speedy -= 2

	# Checar colisiones - ball - borde3
	if pygame.sprite.collide_rect(ball,borde3):
		ball.rect.top = borde3.rect.bottom
		ball.speedy = -ball.speedy
	
	# Checar colisiones - ball - borde4
	if pygame.sprite.collide_rect(ball, borde4):
		if ball.speedx > 0:
			ball.rect.right = borde4.rect.left
			ball.speedx = -ball.speedx
		if ball.speedx < 0:
			ball.rect.left = borde4.rect.right
			ball.speedx = -ball.speedx
	
	# Checar colisiones - ball - borde7
	if pygame.sprite.collide_rect(ball,borde7):
		ball.rect.bottom = borde7.rect.top
		ball.speedy = -ball.speedy

	# Checar colisiones - ball - borde8
	if pygame.sprite.collide_rect(ball,borde8):
		if ball.speedx > 0:
			ball.rect.right = borde8.rect.left
			ball.speedx = -ball.speedx
		if ball.speedx < 0:
			pass
		
	screen.blit(background, [0, 0])
	for w in walls:
		w.draw(screen)
	all_sprites.draw(screen)

	#Marcador
	
	draw_text2(screen, str(score), 25, WIDTH // 2, 10)
	
	pygame.display.flip()

	"""
	self.speedy = 0.9*self.speedy
		self.speedx = 0.9*self.speedx


		# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper1_list, False)
	for hit in hits:
		counter = True
		if counter1:
			counter1 = False
			score += 80
	if not pygame.sprite.collide_rect(ball, bumper1):
		counter1 = True
		
	# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper2_list, False)
	for hit in hits:
		counter = True
		if counter2:
			counter2 = False
			score += 80
	if not pygame.sprite.collide_rect(ball, bumper2):
		counter2 = True
	
	# Checar colisiones - ball - bumper3
	hits = pygame.sprite.spritecollide(ball, bumper3_list, False)
	for hit in hits:
		counter = True
		if counter3:
			counter3 = False
			score += 80
	if not pygame.sprite.collide_rect(ball, bumper3):
		counter3 = True
	

	# Checar colisiones - ball - borde1
	if pygame.sprite.collide_rect(ball, borde1):
		ball.rect.left = borde1.rect.right
		ball.speedx = -ball.speedx
	# Checar colisiones - ball - borde2
	if pygame.sprite.collide_rect(ball, borde2):
		ball.rect.right = borde2.rect.left
		ball.speedx = -ball.speedx
	
	"""