from __future__ import division
import pygame

class Shoot(pygame.sprite.Sprite):
    speed = 7
    damage = 1

    def __init__(self, Player, Game):
        pygame.sprite.Sprite.__init__(self)
        self.game = Game
        self.player = Player
        self.image = pygame.image.load(u'img/bullet-1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.centerx - (self.rect.width / 2)
        self.rect.bottom = self.player.rect.top + 5
    
    def update(self):
        self.rect.y -= 5
        if self.rect.top > 20:
            del self
