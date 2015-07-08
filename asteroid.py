import pygame
from random import randint

class Asteroid(pygame.sprite.Sprite):
    speedx = speedy = 0
    life = 100
    count = 1
    level = 1
    levelAtt = {
            1: {
                u'life': 1,
                u'size': [39, 39],
                u'points': 5,
            },
            2: {
                u'life': 1,
                u'size': [50, 50],
                u'points': 5,
            },
            3: {
                u'life': 2,
                u'size': [75, 75],
                u'points': 15,
            },
            4: {
                u'life': 3,
                u'size': [120, 120],
                u'points': 40,
            },
            5: {
                u'life': 6,
                u'size': [190, 190],
                u'points': 100,
            },
    }
    def __init__(self, level=1):
        pygame.sprite.Sprite.__init__(self)
        #self.sprites = []
        #self.rotation = randint(-5, 5)
        #for i in range(16):
            #if i < 10:
                #i = '0' + str(i)
            #else:
                #i = str(i)
            #self.sprites.append(pygame.image.load('img/a100' + i + '.png'))
        self.image = pygame.image.load(u'img/a10000.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, 
                self.levelAtt[level][u'size'])
        self.life = self.levelAtt[level][u'life']
        self.points = self.levelAtt[level][u'points']
        #self.rect = pygame.mask.from_surface((self.image))
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.count += 1
