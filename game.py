from __future__ import division
import random, sys, pygame, asteroid, explosion, player
from random import randint


class Game(object):
    width, height = 800, 600
    asteroids = pygame.sprite.Group()
    shoots = pygame.sprite.Group()
    explosions = []
    points = 0
    level = 5
    levelAsteroidFrequency = {
            1: 80,
            2: 60,
            3: 40,
            4: 30,
            5: 25,
            6: 10,
    }
    levelUpdateFrequency = {
            2: 25 * 1000,
            3: 50 * 1000,
            4: 75 * 1000,
            5: 110 * 1000,
            6: 150 * 1000,
    }
    asteroidProbability = {
            1: [1],
            2: [1] + [2] * 3,
            3: [1] * 2 + [2] * 3 + [3],
            4: [1] * 3+ [2] * 3 + [3] * 3,
            5: [1] * 3 + [2] * 1 + [3] * 2 + [4] * 5,
            6: [1] * 3 + [2] * 3 + [4] * 2 + [5] * 5,
    }

    def __init__(self):
        pass
    
    def randomAsteroids(self):

        if randint(1, self.levelAsteroidFrequency[self.level])==1:
            astLevel = random.choice(self.asteroidProbability[self.level])

            newasteroid = asteroid.Asteroid(astLevel)

            randx = randint(0, self.screen.get_width() - 50)
            randy = newasteroid.image.get_height() * -1

            newasteroid.rect.x, newasteroid.rect.y = randx, randy
            newasteroid.speedx = randint(-2, 2)
            newasteroid.speedy = randint(1, 2)

            self.asteroids.add(newasteroid)
    
    def initialState(self):
        pygame.init()
        self.font = pygame.font.SysFont(u"monospace", 35)
        self.asteroids.empty()
        self.shoots.empty()
        self.points = 0
        self.level = 1
        self.paused = 0
        self.time = 0

    def gameover(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.run()
                    if event.key == pygame.K_q:
                        sys.exit()

            self.screen.fill((0, 0, 0))
            gameoverLabel = self.font.render(u"Game over", 1, (255, 0, 0))
            pointsLabel = self.font.render(u"Score: " + unicode(self.points),
                    1, (255, 255, 255))
            restartLabel = self.font.render(u"R to restart", 1, (255, 255, 255))
            quitLabel = self.font.render(u"Q to quit", 1, (255, 255, 255))
            self.screen.blit(gameoverLabel, (((self.screen.get_width() - gameoverLabel.get_width()) / 2), 50))
            self.screen.blit(pointsLabel, (((self.screen.get_width() - pointsLabel.get_width()) / 2), 100))
            self.screen.blit(restartLabel, (((self.screen.get_width() - restartLabel.get_width()) / 2), 150))
            self.screen.blit(quitLabel, (((self.screen.get_width() - quitLabel.get_width()) / 2), 200))
            pygame.display.flip()
        print u"Game Over\nPontuacao:", self.points
        sys.exit()
    
    def checkCollision(self):
        #if pygame.sprite.spritecollide(self.p1, self.asteroids, False, pygame.sprite.collide_mask):
            #print('collide', randint(1, 100))
        for shoot in self.shoots:
            collide = pygame.sprite.spritecollide(shoot, self.asteroids,
                    False, pygame.sprite.collide_mask)
            for c in collide:
                self.shoots.remove(shoot)
                c.life -= shoot.damage
                if c.life > 0:
                    expl = explosion.Explosion((shoot.rect.x, shoot.rect.y),
                        (25, 25))
                    #expl.rect.y -= expl.rect.height / 2
                    #expl.rect.x -= expl.rect.width / 2
                    self.explosions.append(expl)
                    break
                expl = explosion.Explosion((c.rect.x, c.rect.y),
                        (c.rect.height, c.rect.width))
                self.explosions.append(expl)
                self.points += c.points
                self.asteroids.remove(c)

        for e in self.explosions:
            done = e.explode()
            if done:
                self.explosions.remove(e)
                e = None

        if pygame.sprite.spritecollide(self.p1, self.asteroids, 
                True, pygame.sprite.collide_mask):
            self.running = False

        #if pygame.sprite.collide_mask(self.p1, self.a):
            #print('collide', randint(1, 100))
        #if pygame.sprite.groupcollide(self.shoots, self.asteroids,  False, pygame.sprite.collide_mask):
            #print("collide")
        
    def score(self):
        self.scoreLabel = self.font.render(u"Score: " + unicode(self.points), 1,
                (255, 255, 200))
        self.levelLabel = self.font.render(u"Level: " + unicode(self.level), 1,
                (255, 255, 200))

    def updateLevel(self):
        tick = self.time
        if self.level+1 in self.levelUpdateFrequency and\
                tick > self.levelUpdateFrequency[self.level+1]:
            self.level += 1

    def pause(self):
        #self.screen.fill((0, 0, 0))
        pauseLabel = self.font.render(u"Paused", 1, (255, 255, 255))
        self.screen.blit(pauseLabel, ((self.screen.get_width() - pauseLabel.get_width()) / 2, 100))
        pygame.display.flip()
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = 0

    def run(self):
        self.initialState()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Galaxy Destroyer")
        self.p1 = player.Player(self)

        self.bg = pygame.image.load(u'img/bg.png')
        self.clock = pygame.time.Clock()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    shoot = self.p1.moveKeyDown(event)
                    if shoot:
                        self.shoots.add(shoot)
                    if event.key == pygame.K_p:
                        self.paused = 1
            if self.paused: self.pause()
            self.score()
            self.updateLevel();
            key = pygame.key.get_pressed()
            self.randomAsteroids()
            self.p1.move(key, self.shoots)
            self.checkCollision()
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.p1.image, self.p1.rect)
            for asteroid in self.asteroids:
                asteroid.update()
                self.screen.blit(asteroid.image, asteroid.rect)
                if asteroid.rect.top > self.screen.get_height() or\
                        (asteroid.rect.right < 0 and asteroid.speedx < 0) or\
                        (asteroid.rect.left > self.screen.get_width() and asteroid.speedx > 0):
                            self.asteroids.remove(asteroid)

            for shoot in self.shoots:
                shoot.update()
                self.screen.blit(shoot.image, shoot.rect)
                if shoot.rect.bottom < 0:
                    self.shoots.remove(shoot)

            
            for e in self.explosions:
                if hasattr(e, u'image'):
                    self.screen.blit(e.image, e.rect)

            
            self.screen.blit(self.levelLabel, (10, 40))
            self.screen.blit(self.scoreLabel, (10, 10))
            self.clock.tick(40)
            pygame.display.flip()
            self.time += self.clock.get_time()

        self.gameover()
