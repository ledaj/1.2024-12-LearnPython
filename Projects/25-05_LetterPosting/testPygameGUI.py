import pygame
import pygame_gui

pygame.init()

# Set up display
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mail Posting Game')

# Set up clock and manager
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# Colors
WHITE = (255, 255, 255)

# Set up UI elements
post_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 500), (100, 50)),
    text='Post Letter',
    manager=manager
)

left_mailbox_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150, 400), (100, 50)),
    text='Left Mailbox',
    manager=manager
)

right_mailbox_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 400), (100, 50)),
    text='Right Mailbox',
    manager=manager
)

# Labels
current_day_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((350, 20), (100, 30)),
    text='Day: 1',
    manager=manager
)

score_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((350, 60), (100, 30)),
    text='Score: 0',
    manager=manager
)

letter_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((300, 120), (200, 30)),
    text='Recipient: Mr. Red',
    manager=manager
)

# Timer Gauge
progress_bar = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((200, 160), (400, 20)),
    start_value=100,
    value_range=(0, 100),
    manager=manager
)

# Game state
running = True
selected_mailbox = None
score = 0
day = 1
timer_value = 100

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                selected_mailbox = 'left'
                left_mailbox_button.select()
                right_mailbox_button.unselect()
            elif event.key == pygame.K_d:
                selected_mailbox = 'right'
                right_mailbox_button.select()
                left_mailbox_button.unselect()
            elif event.key == pygame.K_SPACE:
                if selected_mailbox:
                    print(f'Posted letter to {selected_mailbox} mailbox')
                    score += 1
                    score_label.set_text(f'Score: {score}')

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == left_mailbox_button:
                selected_mailbox = 'left'
                left_mailbox_button.select()
                right_mailbox_button.unselect()
            elif event.ui_element == right_mailbox_button:
                selected_mailbox = 'right'
                right_mailbox_button.select()
                left_mailbox_button.unselect()
            elif event.ui_element == post_button:
                if selected_mailbox:
                    print(f'Posted letter to {selected_mailbox} mailbox')
                    score += 1
                    score_label.set_text(f'Score: {score}')

        manager.process_events(event)

    # Update timer
    timer_value -= time_delta * 20  # adjustable speed
    progress_bar.set_current_value(timer_value)

    if timer_value < 30:
        progress_bar.rebuild()
        progress_bar.background_colour = pygame.Color('#FF0000')  # red
        progress_bar.rebuild()
    else:
        progress_bar.background_colour = pygame.Color('#FFFFFF')  # white
        progress_bar.rebuild()

    manager.update(time_delta)

    window_surface.fill(WHITE)
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
