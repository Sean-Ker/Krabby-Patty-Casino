import argparse
import math
import random
import sys
import time
from os import listdir

import numpy as np
import pygame
import seaborn as sns
import webcolors
from pygame import mixer

from grid_world import Grid, Tile
from matplotlib import pyplot as plt

# Constants
X_GRID = 6              # Width of the grid
Y_GRID = 4              # Height of the grid
LIVES = 3               # How many lives
SHOW_LIVE = True        # Should update the graph live?

# init
pygame.init()
random.seed(1)

# the WIDTH and HEIGHT of each grid
# This sets the margin between each cell
screen = pygame.display.set_mode()
screen_w, screen_h = pygame.display.get_surface().get_size()

programIcon = pygame.image.load('assets\\burger.png')
pygame.display.set_icon(programIcon)

# Define some colors
color_platte = sns.color_palette(["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = webcolors.hex_to_rgb("#9b59b6")

pygame.display.set_caption('Krabby Patty Hunter')
clock = pygame.time.Clock()

# Music and Sound Effects
jump = mixer.Sound('music\\jump.wav')
mixer.music.load('music\\BoxCat_Games-Epic_Song.wav')

plankton_se = []
for s in listdir('music\\plankton_effects'):
    plankton_se.append(mixer.Sound(f'music\\plankton_effects\\{s}'))

# Setup globals for later
grid = None
heart = None
pixels_per_tile = None
margin = None
old_lives = None

# Graph stuff
current_balance = 0     # This is not the starting balance! Starting balance is always 0.
cost_per_game = 10
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
games_log = [] 

# Custom tables. See the report.
rewards_table_441 = {0: 0, 1: 0, 2: 10, 3: 20, 4: 30, 6: 100}   # The custom made rewards table for (4,4,1)
rewards_table_552 = {(2,8):150,(1,8):50,(0,6):30,(0,5):10}      # The custom made rewards table for (5,5,2)

####### print statements for debugging ##############
# print("Right Path: ", grid.path)
# print(grid.player,grid.player.screen_coords())
# print(grid.burger, grid.burger.screen_coords())
# for col in grid.array:
#     for tile in col:
#         print(tile)
# print(grid.actions)
#####################################################
    
# A function to initialize every new round
def initialize_round():
    global grid, screen, heart, pixels_per_tile, margin, old_lives

    pixels_per_tile = int(min(screen_h/Y_GRID,screen_w/X_GRID) * 3 / 4)
    margin = int(pixels_per_tile/20)

    size = [(pixels_per_tile+margin)*X_GRID + margin, (pixels_per_tile+margin)*Y_GRID+margin]
    # print(f"Grid Size: {X_GRID}x{Y_GRID}: ({size[0]}, {size[1]})px")

    setattr(Tile, 'PIXELS_PER_TILE', pixels_per_tile)
    setattr(Tile, 'MARGIN', margin)

    # screen = pygame.display.set_mode(SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE| pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size)

    grid = Grid(X_GRID,Y_GRID,LIVES)
    old_lives = LIVES
    print("Right Path: ", grid.path)

    heart = pygame.image.load(Tile.ASSETS['heart'])
    heart = pygame.transform.scale(heart,(int(pixels_per_tile/2),int(pixels_per_tile/2)))

# Plots a graph of the currents stats
def plot_graph(show_live, games_log):
    all_round_rewards, all_current_balances = ([],[]) if games_log==[] else list(zip(*games_log))
    x = range(len(games_log))
    # print(all_round_rewards,all_current_balances)
    # print(x)
    ax1.plot(x, all_current_balances, label='Accumulated P&L')
    ax1.plot(x, [cost_per_game*(r+1) for r in range(len(games_log))], label = 'Revenue')
    ax2.bar(x, all_round_rewards, label='Profit and Loss')

    # Set titles and labels
    ax1.set_title('Revenue and Profit Over Time')
    ax2.set_xlabel('Time (rounds)')
    ax1.set_ylabel('Price ($)')
    ax2.set_ylabel('Price ($)')

    # Add legend
    if not all_round_rewards == []:
        handles, labels = ax1.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys(), loc='upper left', fancybox=True,shadow=True)

        handles, labels = ax2.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax2.legend(by_label.values(), by_label.keys(), loc='best', fancybox=True,shadow=True)

    # Show final or live graph
    if show_live:
        plt.pause(0.05)
    else:
        plt.show()

# The main game loop. 
def game_loop():
    # print(f'User Grid: {[player.x, player.y]}')
    # print(f'User Coords: {player.screen_coords()}')
    # print(f'Player Size: {player.image.get_size()}')
    global game_over, old_lives, current_balance
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
            mixer.Sound.play(jump)
            # print(grid.score, grid.lives)

            if old_lives != grid.lives:
                mixer.Sound.play(random.choice(plankton_se))
                old_lives = grid.lives

            if grid.done:
                if grid.score == grid.score_max: print("You Won!")

                if X_GRID == 4 and Y_GRID == 4 and LIVES==1:
                    round_reward = cost_per_game-rewards_table_441[grid.score]
                elif X_GRID == 5 and Y_GRID == 5 and LIVES==2:
                    round_reward = cost_per_game-rewards_table_552[grid.score]
                else:
                    continue
                current_balance += round_reward
                print(f'Current P&L: {current_balance}')

                games_log.append([round_reward, current_balance])
                if SHOW_LIVE:
                    plot_graph(True, games_log)

    # return game_over

# A function to draw all of the objects
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
# Scales images to required dimensions.
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

# Function to draw a tile object
def draw(tile):
    screen.blit(preprocess_image(tile.image, pixels_per_tile,
                                 pixels_per_tile), tile.screen_coords())


# The parser for running from the command line
parser = argparse.ArgumentParser()
parser.add_argument('--x', type=int,default=X_GRID, help='The width of the grid')
parser.add_argument('--y', type=int,default=Y_GRID, help='The height of the grid')
parser.add_argument('--l', type=int,default=LIVES, help='The amount of lives')

args = parser.parse_args()
# sys.stdout.write(str(args))

# The main ever-lasting game loop
game_over = False
mixer.music.play(-1)
if (X_GRID == 4 and Y_GRID == 4 and LIVES==1) or (X_GRID == 5 and Y_GRID == 5 and LIVES==2): plot_graph(True, games_log)
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
    mixer.music.stop()
    plot_graph(False, games_log) # Plot final graph!


