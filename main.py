import pygame
import random
import math


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.spaceship = Spaceship(self, 370, 515)
        self.score = 0

        self.enemies = []
        for i in range(12):
            self.enemies.append(Enemy(self, random.randint(0, 736), random.randint(30, 130)))

        self.background = pygame.image.load("stars.png")

        while self.running:
            self.clock.tick(60)
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(-10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_SPACE:
                        self.spaceship.fired()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(-10)

            self.spaceship.update()
            if len(self.spaceship.bullets) > 0:
                for bullet in self.spaceship.bullets:
                    if bullet.fired == True:
                        bullet.update()
                    else:
                        self.spaceship.bullets.remove(bullet)

            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                if enemy.y > 460:
                    for i in self.enemies:
                        i.y = 1000
                        self.game_over()
                    break
            self.print_score()
            pygame.display.update()

    def print_score(self):
        score = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score.render("Score : " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))

    def game_over(self):
        over = pygame.font.Font("freesansbold.ttf", 64)
        over_text = over.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

class Spaceship:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 0
        self.game = game
        self.spaceship_img = pygame.image.load("spaceship.png")
        self.bullets = []

    def fired(self):
        self.bullets.append(Bullet(self.game, self.x, self.y))
        self.bullets[len(self.bullets) - 1].fire()

    def move(self, speed):
        self.change_x += speed

    def update(self):
        self.x += self.change_x
        if self.x < 0:
            self.x = 0
        elif self.x > 736:
            self.x = 736
        self.game.screen.blit(self.spaceship_img, (self.x, self.y))

class Bullet:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.fired = False
        self.bullet_speed = 10
        self.bullet_img = pygame.image.load("fire.png")

    def fire(self):
        self.fired = True

    def update(self):
        self.y -= self.bullet_speed
        if self.y <= 0:
            self.fired = False
        self.game.screen.blit(self.bullet_img, (self.x, self.y))

class Enemy:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 60
        self.game = game
        self.enemy_img = pygame.image.load("enemy.png")

    def check_collision(self):
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt(math.pow(self.x - bullet.x, 2) + math.pow(self.y - bullet.y, 2))
            if distance < 35:
                bullet.fired = False
                self.game.score += 1
                self.x = random.randint(0, 736)
                self.y = random.randint(50, 150)


    def update(self):
        self.x += self.change_x
        if self.x >= 736:
            self.y += self.change_y
            self.change_x = -5
        elif self.x <= 0:
            self.y += self.change_y
            self.change_x = 5
        self.game.screen.blit(self.enemy_img, (self.x, self.y))


if __name__ == "__main__":
    game = Game(800, 600)
    print(len(game.spaceship.bullets))
