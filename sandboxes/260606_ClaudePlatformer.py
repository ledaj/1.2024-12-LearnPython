import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Player settings
PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 0.8

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False
        self.speed = PLAYER_SPEED
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    
        # Keep player on screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        # Reset if player falls off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = 100
            self.rect.y = 400
            self.vel_y = 0
            
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        # Draw simple face
        pygame.draw.circle(screen, WHITE, (self.rect.x + 10, self.rect.y + 15), 5)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 30, self.rect.y + 15), 5)
        pygame.draw.circle(screen, BLACK, (self.rect.x + 10, self.rect.y + 15), 2)
        pygame.draw.circle(screen, BLACK, (self.rect.x + 30, self.rect.y + 15), 2)

class Platform:
    def __init__(self, x, y, width, height, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Basic 2D Platformer")
        self.clock = pygame.time.Clock()
        
        # Create player
        self.player = Player(100, 400)
        
        # Create platforms
        self.platforms = [
            # Ground platforms
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, BROWN),
            # Floating platforms
            Platform(200, 500, 150, 20),
            Platform(400, 400, 120, 20),
            Platform(600, 300, 100, 20),
            Platform(100, 350, 80, 20),
            Platform(350, 250, 100, 20),
            Platform(550, 200, 120, 20),
            Platform(50, 200, 100, 20),
            Platform(700, 450, 80, 20),
        ]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def update(self):
        self.player.update(self.platforms)
        
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Use ARROW KEYS or WASD to move, SPACE to jump", True, BLACK)
        self.screen.blit(text, (10, 10))
        
        text2 = font.render("ESC to quit", True, BLACK)
        self.screen.blit(text2, (10, 50))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()