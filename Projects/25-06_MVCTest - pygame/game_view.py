import pygame

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
BLUE = (50, 150, 255) 
GRAY = (200, 200, 200) 

class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 40)

        self.button_rect = pygame.Rect(100, 100, 200, 60)
        self.reset_rect = pygame.Rect(100, 180, 200, 50)

    def draw(self, score):
        self.screen.fill(WHITE)

        # Score display
        score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text,(100,40))

        # Click button
        pygame.draw.rect(self.screen, BLUE, self.button_rect)
        click_text = self.font.render("Click Me !", True, WHITE)
        self.screen.blit(click_text, (self.button_rect.x + 35, self.button_rect.y + 15))

        # Reset button
        pygame.draw.rect(self.screen, GRAY, self.reset_rect)
        reset_text = self.font.render("Reset", True, BLACK)
        self.screen.blit(reset_text, (self.reset_rect.x + 60, self.reset_rect.y + 10))

        pygame.display.flip()