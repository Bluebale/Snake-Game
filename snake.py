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
        self.color = (246,249,0)
        self.score = 0
        self.state = 'playing'

    def get_head_pos(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.prev_dir:
            return
        self.direction = point
    def move(self):
        cur = self.get_head_pos()
        self.prev_dir = self.direction
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if self.length > 2 and new in self.positions[2:]:
            os.system('afplay ./gameover.wav&')
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
        if self.store == max_score:
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
                r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, self.color, r)
                #pygame.draw.rect(surface, (0, 0, 0), r, 1)
        pygame.draw.circle(surface, (255,255,0), (int(self.positions[0][0] + GRID_SIZE/2), int(self.positions[0][1] + int(GRID_SIZE/2))), int(GRID_SIZE/2),2)

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
                elif event.key == pygame.K_SPACE:
                    self.state = 'playing'

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255,0,25)
        self.randomize_pos()
    def randomize_pos(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    def draw(self, surface):
        food = pygame.image.load('red-apple.png')
        #r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        #pygame.draw.rect(surface, self.color, r)
        surface.blit(food, self.position)

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
            r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (0, 0, 0), r)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH), 0, 32)
    max_score = 0
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    pygame.display.set_caption('Snake')
    drawGrid(surface)
    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("comicsans", 40)
    file = open(HIGHSCORES_FILE, "r")
    max_score = int(file.read())
    file.close()
    
    while(True):
        
        snake.handleKeys()
        surface.fill((0, 0, 0))
        snake.move()
        clock.tick(10 + snake.score/2)
        if snake.get_head_pos() == food.position:
            snake.length += 1
            snake.score += 1
            if snake.score > max_score:
                max_score = snake.score
                file = open(HIGHSCORES_FILE, "w")
                file.write(str(max_score))
                file.close()
            os.system('afplay ./eat.wav&')
            food.randomize_pos()
        if snake.state == 'gameover':
            snake.reset(surface, max_score)
            screen.blit(surface, (0, 0))
        else:
            snake.store = None
            snake.draw(surface)
            food.draw(surface)
            screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
            screen.blit(text, (15, 10))
            text = myfont.render("Highscore {0}".format(max_score), 1, (255, 255, 255))
            screen.blit(text, (280, 10))
        pygame.display.update()

main()