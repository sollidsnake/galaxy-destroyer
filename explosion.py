import pygame

class Explosion(object):
    count = 0
    speed = [0, 0]
    size = [47, 47]
    pos = [0, 0]
    def __init__(self, pos, size=[0, 0]):
        self.pos = pos
        self.size = size
        self.animation = pygame.image.load(u'img/explosion-1.png')
        self.currentFrame = 0
        self.frames = []
        for j in xrange(0, 2):
            j = (j*48) + 1
            for i in xrange(0, 192, 48):
                i = i+1
                self.frames.append(self.animation.subsurface(i, j, 47, 47))
        self.rect = pygame.rect.Rect(pos[0], pos[1], 47, 47)
        #self.rect.x, self.rect.y = pos[0], pos[1]
        if size[0] and size[1]:
            self.setSize(size)
    
    def setSize(self, size):
        for i in xrange(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], size)
            self.rect = pygame.rect.Rect(self.pos[0], self.pos[1],
                    self.size[0], self.size[1])
    
    def explode(self):
        self.count+=1
        if self.currentFrame * 4 < self.count:
            self.currentFrame += 1
        if self.currentFrame >= 8:
            return 1
        self.image = self.frames[self.currentFrame]
        self.rect.y += self.speed[1]
        return 0
