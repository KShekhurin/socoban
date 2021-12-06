import pygame.draw


class Widget:
    def __init__(self):
        pass

    def draw(self, screen):
        pass

    def update(self, events):
        pass


class Gameboard(Widget):
    def __init__(self, board_map):
        self.board_map = board_map

    def draw(self, screen):
        size = pygame.display.get_window_size()
        max_tile_size, mode = min((size[1] // len(self.board_map), "ver"),
                                  (size[0] // len(self.board_map[0]), "hor"))
        print((pygame.display.get_window_size()[0] - max_tile_size * len(self.board_map[0])) / 2)
        x_offset = (size[0] - max_tile_size * len(self.board_map[0])) / 2
        y_offset = (size[1] - max_tile_size * len(self.board_map)) / 2
        for y, row in enumerate(self.board_map):
            for x, tile in enumerate(row):
                position = [
                    (max_tile_size * x),
                    (max_tile_size * y),
                    max_tile_size,
                    max_tile_size,
                ]

                position[0] += x_offset
                position[1] += y_offset

                color = (255, 0, 0)
                if tile == ".":
                    color = (0, 255, 0)

                pygame.draw.rect(screen, color, position)
                #pygame.draw.rect(screen, (0, 0, 0), position, 1)

    def update(self, events):
        pass