import pygame.draw


def get_max_tile_size_and_offsets(height, width):
    size = pygame.display.get_window_size()
    max_tile_size = min(size[1] // height, size[0] // width)
    x_offset = (size[0] - max_tile_size * width) / 2
    y_offset = (size[1] - max_tile_size * height) / 2

    return max_tile_size, x_offset, y_offset


class BoardGenerator:
    def __init__(self, board_map, player_group, barrel_group, wall_group, blockable_group, bg_group, setters_group):
        self.board_map = board_map

        self.player_created = False

        self.bg_group = bg_group
        self.setters_group = setters_group
        self.blockable_group = blockable_group
        self.player_group = player_group
        self.wall_group = wall_group
        self.barrel_group = barrel_group

        self.rect = pygame.rect.Rect((0, 0), (10, 50))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

    def generate(self):
        size = len(self.board_map), len(self.board_map[0])
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        for y, row in enumerate(self.board_map):
            for x, tile in enumerate(row):
                need_bg = True
                if tile == "s":
                    if not self.player_created:
                        Player(x, y, size, self.wall_group, self.barrel_group, self.blockable_group, self.player_group)
                        self.player_created = True
                elif tile == "#":
                    Wall(x, y, size, self.wall_group, self.blockable_group)
                    need_bg = False
                elif tile == "b":
                    Barrel(x, y, size, self.setters_group, self.barrel_group, self.blockable_group)
                elif tile == "x":
                    Setter(x, y, size, self.setters_group)

                if need_bg:
                    Background(x, y, size, self.bg_group)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, game_size, *groups):
        super().__init__(*groups)
        self.x, self.y = x, y
        self.game_size = game_size

        self.rect = pygame.rect.Rect((0, 0), (10, 50))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)


class Player(Tile):
    def __init__(self, x, y, game_size, wall_group, barrel_group, blockable_group, *groups):
        super().__init__(x, y, game_size, *groups)
        self.walls = wall_group
        self.barrels = barrel_group
        self.blocks = blockable_group

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.image.fill((0, 0, 0))

    def will_collide(self, x_offset, y_offset):
        for wall in self.walls:
            if wall.x == self.x + x_offset and wall.y == self.y + y_offset:
                return True
        for barrel in self.barrels:
            if barrel.x == self.x + x_offset and barrel.y == self.y + y_offset:
                for block in self.blocks:
                    if block.x == self.x + 2 * x_offset and block.y == self.y + 2 * y_offset:
                        return True
                barrel.move(x_offset, y_offset)
                return False
        return False

    def update(self, *events):
        events = events[0]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    will_collide = self.will_collide(-1, 0)
                    if not will_collide:
                        self.x -= 1
                elif event.key == pygame.K_RIGHT:
                    will_collide = self.will_collide(1, 0)
                    if not will_collide:
                        self.x += 1
                elif event.key == pygame.K_UP:
                    will_collide = self.will_collide(0, -1)
                    if not will_collide:
                        self.y -= 1
                elif event.key == pygame.K_DOWN:
                    will_collide = self.will_collide(0, 1)
                    if not will_collide:
                        self.y += 1

        self.draw()


class Wall(Tile):
    def __init__(self, x, y, game_size, *groups):
        super().__init__(x, y, game_size, *groups)

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.image.fill((100, 100, 100))

    def update(self, *events):
        self.draw()


class Barrel(Tile):
    def __init__(self, x, y, game_size, setters_group, *groups):
        super().__init__(x, y, game_size, *groups)
        self.setters_group = setters_group

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        if self.on_setter():
            self.image.fill((100, 100, 200))
        else:
            self.image.fill((200, 100, 100))

    def on_setter(self):
        return pygame.sprite.spritecollideany(self, self.setters_group)

    def move(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset

    def update(self, *events):
        self.draw()


class Background(Tile):
    def __init__(self, x, y, game_size, *groups):
        super().__init__(x, y, game_size, *groups)

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.image.fill((0, 255, 0))

    def update(self, *events):
        self.draw()


class Setter(Tile):
    def __init__(self, x, y, game_size, *groups):
        super().__init__(x, y, game_size, *groups)

    def draw(self):
        max_tile_size, x_offset, y_offset = get_max_tile_size_and_offsets(*self.game_size)

        self.rect = pygame.rect.Rect((x_offset + max_tile_size * self.x, y_offset + max_tile_size * self.y),
                                     (max_tile_size, max_tile_size))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)

        self.image.fill((0, 100, 0))

    def update(self, *events):
        self.draw()