import pygame

import sys

from game_controller import GameController


def main():
    pygame.init()
    screen = pygame.display.set_mode((400,300))
    pygame.display.set_caption("Pygame MVC demo")
    clock = pygame.time.Clock()

    controller = GameController(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controller.handle_event(event)

        controller.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
