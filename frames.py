import random

import pygame.display

from widgets import Gameboard


class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self):
        pass

    def update(self, events):
        for updatable in self.updatable:
            updatable.update(events)

    def draw(self, screen):
        for drawable in self.drawable:
            drawable.draw(screen)


class BoardFrame(Frame):
    def __init__(self):
        super().__init__()

    def post_init(self):
        width = random.randint(10, 15)
        game_map = [
            "".join([random.choice([".", "#"]) for i in range(width)])
            for k in range(random.randint(10, 15))
        ]

        size = pygame.display.get_window_size()
        max_tile_size, mode = min((size[1] / len(game_map), "ver"), (size[0] / len(game_map[0]), "hor"))
        self.board = Gameboard(game_map)

        self.drawable.append(self.board)
        self.updatable.append(self.board)