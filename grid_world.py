from game_combinatorics import get_random_path
import numpy as np
import pygame  # Just to load images

# The backend class of the program! 
# Warning: Not documented.
class Grid:
    # (i,j)  i ->  +
    #     j  #  #  #
    #     | #0  1  2
    #     v #1
    #     + #2       X (3,2)

    def __init__(self, x_grid, y_grid, lives, is_machine = False):
        self.width = x_grid
        self.height = y_grid

        self.lives = lives
        self.score = 0
        self.score_max = self.width+self.height-2

        self.is_machine = is_machine

        self.array = self.initialize_grid() # Arrau has an inverse relationship (i,j) => (j,i)
        self.actions = self.initialize_actions()

        self.burger = Tile('burger', self.width-1, 0, is_machine)
        self.plankton = []

        self.i, self.j = (0, self.height-1)
        self.player = Tile('spongebob', self.i, self.j, is_machine)

        self.path = get_random_path(self.width, self.height, True)
        self.done = False

    def initialize_grid(self):
        grid = [[Tile('normal', i, j, self.is_machine) for i in range(self.width)] for j in range(self.height)]
        grid = np.array(grid)
        grid[self.height-1, 0].set_type('visited')
        return grid

    def initialize_actions(self):
        actions = {}
        for j in range(self.height):
            for i in range(self.width):
                pos = [(0,-1), (1,0)]
                if i == self.width-1:
                    pos.remove((1,0))  # Eliminate going right on the right edge
                if j == 0:
                    pos.remove((0,-1))  # Eliminate going up on the upper edge
                actions[(i, j)] = pos
        return actions

    def current_state(self):
        return (self.i, self.j)

    def set_state(self, i, j):
        self.i, self.j = i, j

    # Returns if game is done
    def move(self, di, dj):
        # assert(not self.done)

        action = (di, dj)
        if action not in self.actions[(self.i, self.j)]:
            return

        self.i += action[0]
        self.j += action[1]
        self.array[self.j, self.i].set_type('visited')
        self.player.set_state(self.i, self.j)

        if action == self.path[self.score]:
            self.score += 1
            if self.player == self.burger:
                self.burger = None
                self.done = True
        else:
            self.lives -= 1
            self.plankton.append(Tile('plankton', self.i, self.j, self.is_machine))

            self.i -= action[0]
            self.j -= action[1]
            self.actions[(self.i, self.j)].remove(action)

            self.player.set_state(self.i, self.j)

            # assert(self.lives >= 0)
            if self.lives == 0:
                self.done = True



        # self.x = min(x_grid, self.x)
        # self.x = max(1, self.x)

        # self.y = min(y_grid, self.y)
        # self.y = max(1, self.y)

    # Function for the simulater only.
    # def move_simulation(self, di, dj):
    #     action = (dx, dy)
    #     assert(action in self.actions[(self.i, self.j)])


class Tile:
    # PIXELS_PER_TILE=None
    # MARGIN=None

    ASSETS_DIR = 'assets\\'
    ASSETS = {'spongebob': f'{ASSETS_DIR}spongebob.png',
              'burger': f'{ASSETS_DIR}burger.png',
              'normal': f'{ASSETS_DIR}mystery_box.png',
              'plankton': f'{ASSETS_DIR}plankton.png',
              'visited': f'{ASSETS_DIR}bricks.png',
              'heart': f'{ASSETS_DIR}heart.png'}

    def __init__(self, tile_type, i, j,is_machine):
        self.i = i
        self.j = j
        self.tile_type = tile_type
        # self.image = self.preprocess_image(pygame.load(self.ASSETS[tile_type]), self.PIXELS_PER_TILE, self.PIXELS_PER_TILE)
        if not is_machine:
            self.image = pygame.image.load(self.ASSETS[tile_type])

    def set_type(self, tile_type):
        # self.image = self.preprocess_image(pygame.image.load(self.ASSETS[tile_type]), self.PIXELS_PER_TILE, self.PIXELS_PER_TILE)
        self.image = pygame.image.load(self.ASSETS[tile_type])

    def set_state(self, i, j):
        self.i, self.j = i, j

    def get_state(self):
        return (self.i, self.j)

    def __str__(self):
        return f"{self.tile_type}({self.i}i, {self.j}j)"

    def __eq__(self, other):
        if other != None:
            return self.j == other.j and self.i == other.i
        else:
            return False

    def screen_coords(self):
        return [self.MARGIN + (self.PIXELS_PER_TILE+self.MARGIN) * self.i,
                self.MARGIN + (self.PIXELS_PER_TILE+self.MARGIN) * self.j]
