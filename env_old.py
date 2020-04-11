# Old code, please don't mind



# import pygame
# import pygame.mixer
# import numpy as np
# import time
# import seaborn as sns
# import webcolors
# from game_combinatoric import

# # Constants
# x_grid = 3
# y_grid = 4
# LIVES = 1

# # Define some colors
# flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
# color_platte = sns.color_palette(flatui)
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# PURPLE = webcolors.hex_to_rgb("#9b59b6")

# # the WIDTH and HEIGHT of each grid
# PIXELS_PER_TILE = 100

# LIVES = 1

# ASSETS_DIR = 'assets\\'
# ASSETS = {'spongebob': f'{ASSETS_DIR}spongebob.png',
#           'burger': f'{ASSETS_DIR}burger.png',
#           'normal': f'{ASSETS_DIR}mystery_box.png',
#           'plankton': f'{ASSETS_DIR}plankton.png',
#           'visited': f'{ASSETS_DIR}bricks.png'}

# # This sets the margin between each cell
# MARGIN = 10
# SIZE = [(PIXELS_PER_TILE+MARGIN)*x_grid, (PIXELS_PER_TILE+MARGIN)*y_grid]
# print(f'Grid Size: {SIZE}')

# right_path=('up', 'right', 'right', 'up', 'up', 'right')

# def preporcess_image(image, bx, by):
#     ix, iy = image.get_size()

#     if ix > iy:  # fit to width
#         scale_factor = bx/float(ix)
#         sy = scale_factor * iy
#         if sy > by:
#             scale_factor = by/float(iy)
#             sx = scale_factor * ix
#             sy = by
#         else:
#             sx = bx
#     else:  # fit to height
#         scale_factor = by/float(iy)
#         sx = scale_factor * ix
#         if sx > bx:
#             scale_factor = bx/float(ix)
#             sx = bx
#             sy = scale_factor * iy
#         else:
#             sy = by

#     return pygame.transform.scale(image, (int(sx), int(sy)))

# class Tile_old:

#     def __init__(self, tile_type, x=1, y=1):
#         self.x = x
#         self.y = y
#         self.tile_type = tile_type
#         self.image = preporcess_image(pygame.image.load(
#             ASSETS[tile_type]), PIXELS_PER_TILE, PIXELS_PER_TILE)

#     def __str__(self):
#         return f"{self.x}, {self.y}"

#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y

#     def screen_coords(self):
#         return [(PIXELS_PER_TILE+MARGIN) * (self.x-1),
#                 SIZE[1] - (PIXELS_PER_TILE+MARGIN) * (self.y)]

#     def draw(self):
#         screen.blit(self.image, (self.screen_coords()[0], self.screen_coords()[1]))


# class Blob(Tile):

#     def __init__(self, tile_type, x=1, y=1):
#         super().__init__(tile_type, x, y)

#     def move(self, dx, dy):
#         self.x += dx
#         self.y += dy

#         self.x = min(x_grid, self.x)
#         self.x = max(1, self.x)

#         self.y = min(y_grid, self.y)
#         self.y = max(1, self.y)
#         print(self.x, self.y)


# grid = np.array([[Tile('normal', x, y) for x in range(1,x_grid+1)] for y in range(1,y_grid+1)])

# pygame.init()

# screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
# # SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
# pygame.display.set_caption('Krabby Patty Hunter')
# clock = pygame.time.Clock()

# game_over = False
# player = Blob('spongebob', 1, 1)
# grid[x_grid-1,y_grid-1]= Tile('burger', y_grid, x_grid)


# def game_loop():
#     # print(f'User Grid: {[player.x, player.y]}')
#     # print(f'User Coords: {player.screen_coords()}')
#     # print(f'Player Size: {player.image.get_size()}')

#     game_over = False
#     # pygame.event.pump()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             game_over = True

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 game_over = True
#             elif event.key == pygame.K_RIGHT:
#                 player.move(1, 0)
#             elif event.key == pygame.K_UP:
#                 player.move(0, 1)
#     if grid[player.y-1,player.x-1].tile_type == 'normal':
#         grid[player.y-1,player.x-1] = Tile('visited', player.x, player.y)
#     if grid[player.y-1,player.x-1].tile_type=='burger':
#         print("You Won!")

#     draw_loop()
#     return game_over


# def draw_loop():
#     screen.fill(PURPLE)
#     for row in grid:
#         for tile in row:
#             tile.draw()

#     player.draw()

#     pygame.display.update()
#     clock.tick(60)


# while not game_over:
#     # while LIVES > 0 :
#     game_over = game_loop()
# else:
#     pygame.quit()
#     quit()
