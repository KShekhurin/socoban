import pygame
from frames import Frame

class App:
    def __init__(self, loaded_frame: Frame, start_size=(200, 200)):
        self.start_size = start_size
        self.loaded_frame = loaded_frame

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode(self.start_size, pygame.RESIZABLE)
        run = True

        self.loaded_frame.post_init()

        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False

            screen.fill((0, 0, 255))
            self.loaded_frame.update(events)
            self.loaded_frame.draw(screen)

            pygame.display.flip()