import pygame.display
from widgets import BoardGenerator


class Frame:
    def __init__(self):
        self.drawable = []
        self.updatable = []

    def post_init(self):
        pass

    def append_widget(self, widget):
        self.drawable.append(widget)
        self.updatable.append(widget)

    def append_many_widgets(self, widgets):
        for widget in widgets:
            self.append_widget(widget)

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

        self.blockable_group = pygame.sprite.Group()
        self.bg_group = pygame.sprite.Group()
        self.setters_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.barrels_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        BoardGenerator(
            game_map,
            self.player_group,
            self.barrels_group,
            self.walls_group,
            self.blockable_group,
            self.bg_group,
            self.setters_group
        ).generate()

        self.append_many_widgets([
            self.bg_group,
            self.setters_group,
            self.walls_group,
            self.player_group,
            self.barrels_group,
        ])