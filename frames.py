import random

import pygame.display

from widgets import Player, Gameboard


class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self):
        pass

    def append_widget(self, widget):
        self.drawable.append(widget)
        self.updatable.append(widget)

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
        game_map = [
            "###########",
            "#s........#",
            "#.b..#..b.#",
            "#...x#x...#",
            "#.#######.#",
            "#...x#x...#",
            "#..b.#..b.#",
            "#.........#",
            "###########",
        ]

        self.board_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        Gameboard(game_map, self.player_group, self.board_group)

        self.append_widget(self.board_group)
        self.append_widget(self.player_group)