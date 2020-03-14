import pygame
import pygame.mixer
import numpy as np
import time
import seaborn as sns

# Constants
x_grid = 4
y_grid = 4
LIVES = 1

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# PURPLE =

# the WIDTH and HEIGHT of each grid
PIXELS_PER_TILE = 100

ASSETS_DIR = 'assets'
ASSETS = {'spongebob': f'{ASSETS_DIR}\\spongebob.png',
          'burger': f'{ASSETS_DIR}\\burger.png'}

# This sets the margin between each cell
MARGIN = 0
SIZE = [(PIXELS_PER_TILE+MARGIN)*x_grid, (PIXELS_PER_TILE+MARGIN)*y_grid]
print(f'Grid Size: {SIZE}')


def preporcess_image(image, bx, by):
    ix, iy = image.get_size()

    if ix > iy:  # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:  # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(image, (int(sx), int(sy)))


class Blob:

    def __init__(self, image_path, x=1, y=1):
        self.x = x
        self.y = y
        self.image = preporcess_image(pygame.image.load(
            image_path), PIXELS_PER_TILE, PIXELS_PER_TILE)

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def game_coords(self):
        return [SIZE[0] - (PIXELS_PER_TILE+MARGIN) * (self.x-1),
                (PIXELS_PER_TILE+MARGIN) * (self.y-1)]

    # def draw_coords(self):

    def move(self, dx, dy):
        self.x = min(x_grid, self.x + dx)
        self.x = max(1, self.x+dx)

        self.y = min(y_grid, self.y + dy)
        self.y = max(1, self.y+dy)

    def draw(self):
        screen.blit(self.image, (self.get_coords()[0], self.get_coords()[1]))

# grid = np.zeros()


pygame.init()

screen = pygame.display.set_mode(SIZE)
# SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
pygame.display.set_caption('Krabby Patty Hunter')
clock = pygame.time.Clock()

game_over = False
player = Blob(ASSETS['spongebob'], 1, 1)
burger = Blob(ASSETS['burger'], x_grid, y_grid)


def game_loop():
    print(f'User Grid: {[player.x, player.y]}')
    print(f'User Coords: {player.get_coords()}')
    # print(f'Player Size: {player.image.get_size()}')

    game_over = False
    # pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_UP:
                player.move(0, 1)
    draw_loop()
    return game_over


def draw_loop():
    screen.fill(WHITE)
    player.draw()
    burger.draw()
    pygame.display.update()
    clock.tick(60)


while not game_over:
    game_over = game_loop()
else:
    pygame.quit()
    quit()
