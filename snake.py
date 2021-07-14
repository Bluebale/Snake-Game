#Simple snake game using pygame
import random
import sys
import os
import pygame

HIGHSCORES_FILE = 'highscores.txt'

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.prev_dir = self.direction
        self.color = BLUE
        self.score = 0
        self.state = 'playing'

    def get_head_pos(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.prev_dir:
            return
        self.direction = point
    def move(self, max_score):
        cur = self.get_head_pos()
        self.prev_dir = self.direction
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if self.length > 2 and new in self.positions[2:]:
            if self.score > max_score:
                os.system('afplay ./sounds/victory.mp3&')
            else:
                os.system('afplay ./sounds/gameover.wav&')
            self.state = 'gameover'
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    def reset(self, surface, max_score):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.prev_dir = self.direction
        if self.store is None:
            self.store = self.score
        self.score = 0
        surface.fill((0,0,0))
        font = pygame.font.SysFont("comicsans", 60)
        if self.store > max_score:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render('NEW HIGHSCORE!', 1, (246,249,0))
            surface.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height())//2-40))
        else:
            text = font.render('Game Over', 1, (246,249,0))
            surface.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height())//2-40))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render('Score = {}'.format(self.store), 1, (255,255,255))
        surface.blit(text, ((SCREEN_WIDTH-text.get_width())//2,(SCREEN_HEIGHT-text.get_height())//2))
        font = pygame.font.SysFont("arial", 20)
        text = font.render('>>Press SPACE_BAR to play again', 1, (255,255,255))
        surface.blit(text, ((SCREEN_WIDTH-text.get_width())-20,(SCREEN_HEIGHT-text.get_height())-40))
    def draw(self, surface):
        for p in self.positions:
            if p != self.positions[0]:
                r = pygame.Rect((int(p[0]), int(p[1])), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, BLACK, r, 1)
        pygame.draw.circle(surface, BLUE, (int(self.positions[0][0] + GRID_SIZE/2), int(self.positions[0][1] + int(GRID_SIZE/2))), int(GRID_SIZE/2))
        pygame.draw.circle(surface, BLACK, (int(self.positions[0][0] + GRID_SIZE/2), int(self.positions[0][1] + int(GRID_SIZE/2))), int(GRID_SIZE/2),2)

    def handleKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    self.turn(UP)
                elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    self.turn(DOWN)
                elif (event.key == pygame.K_LEFT )or (event.key == pygame.K_a):
                    self.turn(LEFT)
                elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    self.turn(RIGHT)
                elif event.key == pygame.K_SPACE:
                    self.state = 'playing'

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = YELLOW
        self.randomize_pos()
    def randomize_pos(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(2, GRID_HEIGHT - 1) * GRID_SIZE)
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (26,93,191)
BLUE = (250,215,68)

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH), 0, 32)
    max_score = 0
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    pygame.display.set_caption('Snake')
    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("comicsans", 40)
    with open(HIGHSCORES_FILE, "r") as file:
        max_score = int(file.read())
    
    while(True):
        snake.handleKeys()
        surface.fill((0, 0, 0))
        snake.move(max_score)
        clock.tick(10 + snake.score/1.5)
        if snake.get_head_pos() == food.position:
            snake.length += 1
            snake.score += 1
            os.system('afplay ./sounds/eat.mp3&')
            food.randomize_pos()
            with open(HIGHSCORES_FILE, "r") as file:
                max_score = int(file.read())
        if snake.state == 'gameover':
            if snake.score > max_score:
                file = open(HIGHSCORES_FILE, "w")
                file.write(str(snake.score))
                file.close()
            snake.reset(surface, max_score)
            screen.blit(surface, (0, 0))
        else:
            snake.store = None
            food.draw(surface)
            snake.draw(surface)
            screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
            screen.blit(text, (15, 10))
            text = myfont.render("Highscore {0}".format(max_score), 1, (255, 255, 255))
            screen.blit(text, (280, 10))
        pygame.display.update()

main()