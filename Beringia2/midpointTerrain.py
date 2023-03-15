import pygame
import random

# Define some constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MAX_HEIGHT = 200
ROUGHNESS = 0.5

# Initialize Pygame
pygame.init()

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define the colors we will use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define a function to calculate the midpoint value
def midpoint(left, right):
    return (left + right) / 2 + (random.random() - 0.5) * MAX_HEIGHT * ROUGHNESS

# Define a function to generate the terrain map
def generate_terrain_map(width):
    map = [0] * width
    map[0] = random.randint(0, MAX_HEIGHT)
    map[-1] = random.randint(0, MAX_HEIGHT)
    step_size = width - 1
    while step_size > 1:
        half_step = step_size // 2
        for i in range(half_step, width - 1, step_size):
            map[i] = midpoint(map[i - half_step], map[i + half_step])
            if map[i] < 0:
                map[i] = 0
            if map[i] > MAX_HEIGHT:
                map[i] = MAX_HEIGHT
        step_size //= 2
    return map

# Generate the terrain map
terrain_map = generate_terrain_map(WINDOW_WIDTH)

# Draw the terrain
for i in range(WINDOW_WIDTH - 1):
    pygame.draw.line(window, WHITE, (i, WINDOW_HEIGHT - terrain_map[i]), (i + 1, WINDOW_HEIGHT - terrain_map[i + 1]))

# Update the display
pygame.display.flip()

# Wait for the user to close the window
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

# Clean up Pygame
pygame.quit()