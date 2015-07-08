from __future__ import division
import pygame, shoot

class Player(pygame.sprite.Sprite):
    speed = 4
    shootInterval = 450
    lastShoot = shootInterval * -1
    k_right = set([pygame.K_RIGHT])
    k_left = set([pygame.K_LEFT])
    k_up = set([pygame.K_UP])
    k_down = set([pygame.K_DOWN])
    def __init__(self, Game):
        pygame.sprite.Sprite.__init__(self)
        self.shoots = pygame.sprite.Group()
        self.game = Game
        self.image = pygame.image.load(u'img/destroyer.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = (self.game.width - self.rect.width) / 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = self.game.height - 20
    
    def move(self, key, shoots):
        pressed = set([i for i, x in enumerate(key) if x==1])
        if bool(self.k_right.intersection(pressed)) and self.rect.right < self.game.width:
            self.rect.x += self.speed
        if bool(self.k_up.intersection(pressed)) and self.rect.top > 0:
            self.rect.y -= self.speed
        if bool(self.k_down.intersection(pressed)) and self.rect.bottom < self.game.height:
            self.rect.y += self.speed
        if bool(self.k_left.intersection(pressed)) and self.rect.left > 0:
            self.rect.x -= self.speed
        #if key[pygame.K_SPACE]:
            #shoots.add(shoot.Shoot(self, self.game))

    def moveKeyDown(self, event):
        if event.key == pygame.K_SPACE and\
                self.lastShoot + self.shootInterval < pygame.time.get_ticks():
            self.lastShoot = pygame.time.get_ticks()
            return shoot.Shoot(self, self.game)
        return False
