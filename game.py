import pygame
import math
import sys
import pygame.mixer
import numpy as np
import time
import seaborn as sns
import webcolors
from grid_world import Grid, Tile
import argparse

# Constants
X_GRID = 4
Y_GRID = 4
LIVES = 1

pygame.init()

# the WIDTH and HEIGHT of each grid
# This sets the margin between each cell
screen = pygame.display.set_mode()
screen_w, screen_h = pygame.display.get_surface().get_size()

# Define some colors
color_platte = sns.color_palette(["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIVES
PURPLE = webcolors.hex_to_rgb("#9b59b6")

pygame.display.set_caption('Krabby Patty Hunter')
clock = pygame.time.Clock()

grid = None
heart = None
pixels_per_tile = None
margin = None
# print("Right Path: ", grid.path)
# print(grid.player,grid.player.screen_coords())
# print(grid.burger, grid.burger.screen_coords())
# for col in grid.array:
#     for tile in col:
#         print(tile)
# print(grid.actions)

    

def initialize_round():
    global grid, screen, heart, pixels_per_tile, margin

    pixels_per_tile = int(min(screen_h/Y_GRID,screen_w/X_GRID) * 3 / 4)
    margin = int(pixels_per_tile/20)

    size = [(pixels_per_tile+margin)*X_GRID + margin, (pixels_per_tile+margin)*Y_GRID+margin]
    print(f"Grid Size: {X_GRID}x{Y_GRID}: ({size[0]}, {size[1]})px")


    setattr(Tile, 'PIXELS_PER_TILE', pixels_per_tile)
    setattr(Tile, 'MARGIN', margin)

    # screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE| pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size)

    grid = Grid(X_GRID,Y_GRID,LIVES)
    # print("Right Path: ", grid.path)

    heart = pygame.image.load(Tile.ASSETS['heart'])
    heart = pygame.transform.scale(heart,(int(pixels_per_tile/2),int(pixels_per_tile/2)))


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
        screen.blit(heart,(margin + i*(heart.get_width())+margin*i%2,margin))

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
    screen.blit(preprocess_image(tile.image, pixels_per_tile,
                                 pixels_per_tile), tile.screen_coords())



parser = argparse.ArgumentParser()
parser.add_argument('--x', type=int,default=X_GRID, help='The width of the grid')
parser.add_argument('--y', type=int,default=Y_GRID, help='The height of the grid')
parser.add_argument('--l', type=int,default=LIVES, help='The amount of lives')

args = parser.parse_args()
# sys.stdout.write(str(args))

game_over = False
while not game_over:
    X_GRID,Y_GRID,LIVES = args.x, args.y, args.l
    initialize_round()
    while not grid.done and not game_over:
        game_loop()
        draw_loop()
    else:
        print(f'Score: {grid.score}')
else:
    pygame.quit()
    quit()


