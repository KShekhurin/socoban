import pygame.draw


def get_max_tile_size_and_offsets(height, width):
    size = pygame.display.get_window_size()
    max_tile_size = min(size[1] // height, size[0] // width)
    x_offset = (size[0] - max_tile_size * width) / 2
    y_offset = (size[1] - max_tile_size * height) / 2

    return max_tile_size, x_offset, y_offset


class Gameboard(pygame.sprite.Sprite):
    def __init__(self, board_map, player_group, *groups):
        super().__init__(*groups)
        self.board_map = board_map

        self.player_group = player_group
        self.player_created = False

        self.rect = pygame.rect.Rect((0, 0), (10, 50))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def draw(self):
        size = len(self.board_map), len(self.board_map[0])
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*size)

        self.rect = pygame.rect.Rect((x_offset, y_offset), (max_tile_size * size[1], max_tile_size * size[0]))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        for y, row in enumerate(self.board_map):
            for x, tile in enumerate(row):
                position = [
                    max_tile_size * x,
                    max_tile_size * y,
                    max_tile_size,
                    max_tile_size,
                ]

                color = (255, 0, 0)
                if tile == ".":
                    color = (0, 255, 0)
                elif tile == "s":
                    color = (0, 255, 0)
                    if not self.player_created:
                        Player(x, y, size, self.player_group)
                        self.player_created = True
                elif tile == "x":
                    color = (100, 100, 100)
                elif tile == "b":
                    color = (200, 100, 100)

                pygame.draw.rect(self.image, color, position)

    def update(self, *events):
        self.draw()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game_size, *groups):
        super().__init__(*groups)
        self.x, self.y = x, y
        self.game_size = game_size

        self.rect = pygame.rect.Rect((0, 0), (10, 50))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.image.fill((0, 0, 0))

    def update(self, *events):
        events = events[0]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.x += 1
                elif event.key == pygame.K_UP:
                    self.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.y += 1

        self.draw()