import pygame
import math
import pygame.mixer
import numpy as np
import time
import seaborn as sns
import webcolors
from grid_world import Grid, Tile

# Constants
x_grid = 6
y_grid = 6
LIVES = 4

# the WIDTH and HEIGHT of each grid
# This sets the margin between each cell
PIXELS_PER_TILE = 160
MARGIN = 10

# Define some colors
color_platte = sns.color_palette(["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = webcolors.hex_to_rgb("#9b59b6")


SIZE = [(PIXELS_PER_TILE+MARGIN)*x_grid + MARGIN, (PIXELS_PER_TILE+MARGIN)*y_grid+MARGIN]
print(f"Grid Size: {x_grid}x{y_grid}: ({SIZE[0]}, {SIZE[1]})px")

pygame.init()

screen = pygame.display.set_mode(SIZE)
# screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE| pygame.FULLSCREEN)
pygame.display.set_caption('Krabby Patty Hunter')
clock = pygame.time.Clock()

setattr(Tile, 'PIXELS_PER_TILE', PIXELS_PER_TILE)
setattr(Tile, 'MARGIN', MARGIN)

grid = None
# print("Right Path: ", grid.path)
# print(grid.player,grid.player.screen_coords())
# print(grid.burger, grid.burger.screen_coords())
# for col in grid.array:
#     for tile in col:
#         print(tile)
# print(grid.actions)

heart = pygame.image.load(Tile.ASSETS['heart'])
heart = pygame.transform.scale(heart,(int(PIXELS_PER_TILE/2),int(PIXELS_PER_TILE/2)))

def initialize_round():
    global grid
    grid = Grid(x_grid, y_grid, lives=LIVES)
    print("Right Path: ", grid.path)
    # print(grid.score_max)


def game_loop():
    # print(f'User Grid: {[player.x, player.y]}')
    # print(f'User Coords: {player.screen_coords()}')
    # print(f'Player Size: {player.image.get_size()}')
    global game_over
    # pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_RIGHT:
                grid.move(1, 0)
            elif event.key == pygame.K_UP:
                grid.move(0, -1)
            print(grid.score, grid.lives)

            if grid.done and grid.score == grid.score_max:
                print("You Won!")
    # return game_over


def draw_loop():
    screen.fill(PURPLE)

    for col in grid.array:
        for tile in col:
            draw(tile)

    if not grid.burger == None:
        draw(grid.burger)

    for plank in grid.plankton:
        draw(plank)

    draw(grid.player)
    for i in range(grid.lives):
        screen.blit(heart,(MARGIN + i*(heart.get_width())+MARGIN*i%2,MARGIN))

    pygame.display.update()
    clock.tick(60)

# Contributed code by pygame.com
def preprocess_image(asset, bx, by):
    ix, iy = asset.get_size()

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

    return pygame.transform.scale(asset, (int(sx), int(sy)))


def draw(tile):
    screen.blit(preprocess_image(tile.image, PIXELS_PER_TILE,
                                 PIXELS_PER_TILE), tile.screen_coords())


game_over = False
while not game_over:
    initialize_round()
    while not grid.done and not game_over:
        game_loop()
        draw_loop()
    else:
        print(f'Score: {grid.score}')
else:
    pygame.quit()
    quit()
