from pygame import *
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
picture = transform.scale(image.load('fon.png'), (win_width, win_height))
back = (195, 132, 255)
window.fill(back)
win = transform.scale(image.load('heavenfon(2).jpg'), (win_width, win_height))
lose = transform.scale(image.load('oblivion.jpg'), (win_width, win_height))
display.set_caption('Way2Heaven')


class GameSprite(sprite.Sprite):
	def __init__(self,width,height,x,y,picture): 
		super().__init__()
		self.image = transform.scale(image.load(picture), (width, height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
	def __init__(self,width,height,x,y,picture, speed_x, speed_y):
		super().__init__(width,height,x,y,picture)
		self.speed_x = speed_x
		self.speed_y = speed_y
	def update(self):
		self.rect.x += self.speed_x
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > win_width:
			self.rect.right = win_width

		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > win_height:
			self.rect.bottom = win_height

		platforms_touched = sprite.spritecollide(self, barriers, False)
		if self.speed_x > 0:
			for p in platforms_touched:
				self.rect.right = min(self.rect.right, p.rect.left)
		elif self.speed_x < 0:
			for p in platforms_touched:
				self.rect.left = max(self.rect.left, p.rect.right)
		self.rect.y += self.speed_y
		platforms_touched = sprite.spritecollide(self, barriers, False)
		if self.speed_y > 0:
			for p in platforms_touched:
				self.rect.bottom = min(self.rect.bottom, p.rect.top)
		elif self.speed_y < 0:
			for p in platforms_touched:
				self.rect.top = max(self.rect.top, p.rect.bottom)		
	def fire(self):
		bullet = Bullet(30, 30, self.rect.left, self.rect.centery, 'light1.png', 15)
		bullets.add(bullet)



class Enemy(GameSprite):
	def __init__(self,width,height,x,y,picture, speed_x, speed_y):
		super().__init__(width,height,x,y,picture)
		self.speed_y = speed_y
	def update(self):
		if self.rect.y <= 0:
			self.direction = 'right'
		if self.rect.y >= win_height - 170:
			self.direction = 'left'
		if self.direction == 'left':
			self.rect.y -= self.speed_y
		else:
			self.rect.y += self.speed_y

class Bullet(GameSprite):
	def __init__(self,width,height,x,y,picture, speed_x):
		super().__init__(width,height,x,y,picture)
		self.speed_x = speed_x
	def update(self):
		self.rect.x += self.speed_x
		if self.rect.x >= 700:
			self.kill()
	

wall_1 = GameSprite(110,300,200,230, 'icloud(3).png')
wall_2 = GameSprite(300,110,420,200, 'icloud.png')
wall_3 = GameSprite(110,300,200,-170, 'icloud(3).png')
player1 = Player(70,70,0,0, 'angel (2).png', 0,0)
final = GameSprite(100,100,560,380, 'heaven.png')
barriers = sprite.Group()
devil1 = Enemy(70,70,320,0, 'devil.png', 0,10)

enemies = sprite.Group()
enemies.add(devil1)

barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)

money = 0
money_1 = GameSprite(40, 40, 600, 30, 'money.png')
money_2 = GameSprite(40, 40, 550, 60, 'money.png')
money_3 = GameSprite(40, 40, 90, 400, 'money.png')
money_4 = GameSprite(40, 40, 220, 160, 'money.png')

money_group = sprite.Group()
money_group.add(money_1)
money_group.add(money_2)
money_group.add(money_3)
money_group.add(money_4)

font.init()
font1 = font.SysFont('Verdana', 30)
text_score = font1.render("Счёт: " + str(money), True, (0,0,0))


run = True
finish = False
while run:
	if finish != True:
		text_score = font1.render("Счёт: " + str(money), True, (0,0,0))
		window.blit(picture,(0,0))
		barriers.draw(window)
		player1.reset()
		final.reset()
		bullets.draw(window)
		enemies.draw(window)
		money_group.draw(window)
		window.blit(text_score, (40, 40))
		sprite.groupcollide(bullets, barriers, True, False)
		sprite.groupcollide(bullets, enemies, True, True)
		if sprite.spritecollide(player1, enemies, True):
			finish = True
			window.blit(lose, (0,0))
		time.delay(50)
		if sprite.collide_rect(player1, final):
			finish = True
			window.blit(win, (0,0))

		if sprite.spritecollide(player1, money_group, True):
			money += 1

	for e in event.get():
		if e.type == QUIT:
			run = False
		elif e.type == KEYDOWN:
			if e.key == K_w:
				player1.speed_y = -10
			if e.key == K_d:
				player1.speed_x = 10
			if e.key == K_s:
				player1.speed_y = 10
			if e.key == K_a:
				player1.speed_x = -10
		elif e.type == KEYUP:
			if e.key == K_w:
				player1.speed_y = 0
			if e.key == K_d:
				player1.speed_x = 0
			if e.key == K_s:
				player1.speed_y = 0
			if e.key == K_a:
				player1.speed_x = 0
			if e.key == K_SPACE:
				player1.fire()
	player1.update()
	display.update()
	enemies.update()
	bullets.update()