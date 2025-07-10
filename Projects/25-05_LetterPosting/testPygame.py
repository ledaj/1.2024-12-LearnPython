import pygame
import csv
import time
import os
import sys

# ---------------- DATA CLASSES ----------------
class Letter:
    def __init__(self, letterID, recipientID, day):
        self.letterID = letterID
        self.recipientID = recipientID
        self.day = int(day)
        self.postedID = ""
        self.is_mailed = False

    def mail(self, postedID):
        self.postedID = postedID
        self.is_mailed = True


class Mailbox:
    def __init__(self, boxID, address, screen, color="white"):
        self.boxID = boxID
        self.address = address
        self.has_mail = False
        self.color = color
        self.screen = int(screen)
        self.containing = []

    def receiveMail(self, letter):
        self.containing.append(letter)
        self.has_mail = True


# ---------------- GAME CLASS ----------------
class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("mailPoster")

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

        # Paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.letters_path = os.path.join(self.BASE_DIR, "Letters.csv")
        self.mailboxes_path = os.path.join(self.BASE_DIR, "Mailboxes.csv")

        # Game State
        self.score = 0
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        self.missed_count = 0
        self.day_duration = 10
        self.current_day = 1
        self.is_game_running = False
        self.current_screen = 0

        # Data
        self.all_letters = self.load_letters(self.letters_path)
        self.mailboxes = self.load_mailboxes(self.mailboxes_path)
        self.letters_today = []
        self.current_letter_index = 0

        self.clock = pygame.time.Clock()
        self.day_start_time = 0

        self.run_game()

    def load_letters(self, filename):
        letters = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    letters.append(Letter(row['letterID'], row['recipientID'], row['day']))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return letters

    def load_mailboxes(self, filename):
        mailboxes = []
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    mailboxes.append(Mailbox(row['boxID'], row['address'], row['screen'], row.get('color', 'white')))
        except FileNotFoundError:
            print(f"Error: Could not find {filename}")
        return mailboxes

    def start_day(self):
        self.is_game_running = True
        self.day_start_time = time.time()
        self.letters_today = [l for l in self.all_letters if l.day == self.current_day]
        self.current_letter_index = 0
        self.letters_delivered = 0

    def end_day(self):
        self.is_game_running = False
        self.current_day += 1

    def get_current_letter(self):
        if self.current_letter_index < len(self.letters_today):
            return self.letters_today[self.current_letter_index]
        return None

    def post_letter(self, mailbox):
        if not self.is_game_running:
            return
        letter = self.get_current_letter()
        if not letter:
            return

        letter.mail(mailbox.boxID)
        mailbox.receiveMail(letter)

        if letter.recipientID == mailbox.boxID:
            self.score += 1
        else:
            self.wrong_deliveries += 1
        self.letters_delivered += 1
        self.current_letter_index += 1

        if self.current_letter_index >= len(self.letters_today):
            self.end_day()

    def draw_text(self, text, x, y, font=None, color=(255, 255, 255)):
        if font is None:
            font = self.font
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def draw_mailboxes(self):
        screen_mailboxes = [mb for mb in self.mailboxes if mb.screen == self.current_screen]
        start_x = 100
        y = 400
        box_width = 200
        box_height = 50
        for i, mb in enumerate(screen_mailboxes):
            rect = pygame.Rect(start_x + i * (box_width + 50), y, box_width, box_height)
            color = pygame.Color(mb.color) if hasattr(pygame.Color, mb.color) else pygame.Color("gray")
            pygame.draw.rect(self.screen, color, rect)
            self.draw_text(mb.address, rect.x + 10, rect.y + 10, self.small_font)
            mb.rect = rect  # attach to mailbox for click detection

    def handle_click(self, pos):
        for mb in self.mailboxes:
            if hasattr(mb, 'rect') and mb.rect.collidepoint(pos):
                self.post_letter(mb)

    def run_game(self):
        running = True
        while running:
            self.screen.fill((0, 0, 30))  # Dark blue bg
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_day()
                    elif event.key == pygame.K_a:
                        self.current_screen = max(0, self.current_screen - 1)
                    elif event.key == pygame.K_e:
                        self.current_screen += 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            # UI
            self.draw_text(f"Day {self.current_day}", 20, 20)
            self.draw_text(f"Score: {self.score} | Wrong: {self.wrong_deliveries}", 20, 50)

            if self.is_game_running:
                remaining = max(0, self.day_duration - (time.time() - self.day_start_time))
                self.draw_text(f"Time Left: {remaining:.1f}s", 20, 80)

                letter = self.get_current_letter()
                if letter:
                    recipient_box = next((mb for mb in self.mailboxes if mb.boxID == letter.recipientID), None)
                    recipient_address = recipient_box.address if recipient_box else f"ID {letter.recipientID}"
                    self.draw_text(f"Letter for: {recipient_address}", 20, 110)
                else:
                    self.draw_text("All letters delivered.", 20, 110)

                if remaining <= 0:
                    self.end_day()

            else:
                self.draw_text("Press SPACE to Start", 20, 110)

            self.draw_mailboxes()

            pygame.display.flip()
            self.clock.tick(60)


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    Game()
