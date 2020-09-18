#Simple snake game using pygame
import pygame
import random
import sys
import os
import shelve

HIGHSCORES_FILE = 'highscores.txt'

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (246,249,0)
        self.score = 0

    def get_head_pos(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    def move(self):
        cur = self.get_head_pos()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if self.length > 2 and new in self.positions[2:]:
            os.system('afplay ./gameover.wav&')
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        pygame.time.delay(3000)
    def draw(self, surface):
        for p in self.positions:
            if p != self.positions[0]:
                r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, self.color, r)
                #pygame.draw.rect(surface, (0, 0, 0), r, 1)
        pygame.draw.circle(surface, (255,255,0), (self.positions[0][0] + GRID_SIZE/2, self.positions[0][1] + GRID_SIZE/2), GRID_SIZE/2,2)

    def handleKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255,0,25)
        self.randomize_pos()
    def randomize_pos(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            #if(x + y) % 2 == 0:
            r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (0, 0, 0), r)
            #else:
              #  rr = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
               # pygame.draw.rect(surface, (84, 194, 205), rr)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    pygame.display.set_caption('Snake')
    drawGrid(surface)
    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("monospace", 25)
    
    
    while(True):
        snake.handleKeys()
        surface.fill((0, 0, 0))
        snake.move()
        if snake.score < 20:
            clock.tick(10 + snake.score/2)
        else:
            clock.tick(20 + snake.score/10)
        if snake.get_head_pos() == food.position:
            snake.length += 1
            snake.score += 1
            os.system('afplay ./bounce.wav&')
            food.randomize_pos()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
        screen.blit(text, (15, 10))
        pygame.display.update()

main()