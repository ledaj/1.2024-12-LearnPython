import pygame

from game_model import GameModel 
from game_view import GameView


class GameController:
    def __init__(self, screen):
        self.model = GameModel()
        self.view = GameView(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.view.button_rect.collidepoint(pos):
                self.model.increase_score()
            elif self.view.reset_rect.collidepoint(pos):
                self.model.reset_score()

    def update(self):
        self.view.draw(self.model.score)