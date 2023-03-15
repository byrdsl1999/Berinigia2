import pygame

# Define the dimensions of the screen and the panel
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PANEL_HEIGHT = 100

# Define the colors to be used
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Create the Pygame screen and set its title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Empty Screen with Buttons")

# Create a panel surface with a gray background and buttons
panel = pygame.Surface((SCREEN_WIDTH, PANEL_HEIGHT))
panel.fill(GRAY)

# Add three green buttons to the panel
button_width = 80
button_height = 40
button_spacing = 20
button_left_margin = (SCREEN_WIDTH - 3 * button_width - 2 * button_spacing) // 2

button_1_rect = pygame.Rect(button_left_margin, PANEL_HEIGHT // 2 - button_height // 2, button_width, button_height)
button_2_rect = pygame.Rect(button_left_margin + button_width + button_spacing, PANEL_HEIGHT // 2 - button_height // 2, button_width, button_height)
button_3_rect = pygame.Rect(button_left_margin + 2 * (button_width + button_spacing), PANEL_HEIGHT // 2 - button_height // 2, button_width, button_height)

pygame.draw.rect(panel, GREEN, button_1_rect)
pygame.draw.rect(panel, GREEN, button_2_rect)
pygame.draw.rect(panel, GREEN, button_3_rect)

# Add labels to the buttons
font = pygame.font.SysFont("Arial", 16)
button_1_label = font.render("Button 1", True, WHITE)
button_2_label = font.render("Button 2", True, WHITE)
button_3_label = font.render("Button 3", True, WHITE)

panel.blit(button_1_label, (button_1_rect.x + button_width // 2 - button_1_label.get_width() // 2, button_1_rect.y + button_height // 2 - button_1_label.get_height() // 2))
panel.blit(button_2_label, (button_2_rect.x + button_width // 2 - button_2_label.get_width() // 2, button_2_rect.y + button_height // 2 - button_2_label.get_height() // 2))
panel.blit(button_3_label, (button_3_rect.x + button_width // 2 - button_3_label.get_width() // 2, button_3_rect.y + button_height // 2 - button_3_label.get_height() // 2))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the panel and update the screen
    screen.fill(WHITE)
    screen.blit(panel, (0, SCREEN_HEIGHT - PANEL_HEIGHT))
    pygame.display.flip()

# Quit Pygame properly when the game loop ends
pygame.quit()