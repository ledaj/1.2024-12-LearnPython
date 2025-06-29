from game_model import GameModel 
from game_view import GameView


class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root, self)

    def on_click(self):
        self.model.increase_score()
        self.view.update_score(self.model.score)

    def on_reset(self):
        self.model.reset_score()
        self.view.update_score(self.model.score)
