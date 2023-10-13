import random
import pygame

# Define the grid size and cell size
GRID_SIZE = 20
CELL_SIZE = 20

# Define the colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Define the growth rate for the trees
GROWTH_RATE = 0.1

# Initialize the Pygame module
pygame.init()

# Set the screen size and title
SCREEN_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Hex Grid Forest Growth Simulation")

# Define a function to get the color of a hex cell based on its growth
def get_color(growth):
    if growth < 0.2:
        return WHITE
    else:
        return GREEN

# Define the initial grid with all cells having a growth of 0
grid = [[0 for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the grid by adding growth to each cell
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            grid[x][y] += GROWTH_RATE * random.random()

    # Draw the grid on the screen
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Calculate the position of the cell on the screen
            pos_x = CELL_SIZE * x + CELL_SIZE * 0.5 * (y % 2)
            pos_y = CELL_SIZE * y * 0.75

            # Get the color of the cell based on its growth
            color = get_color(grid[x][y])

            # Draw the hexagon cell
            pygame.draw.polygon(screen, color, [
                (pos_x + CELL_SIZE * 0.5, pos_y),
                (pos_x + CELL_SIZE, pos_y + CELL_SIZE * 0.25),
                (pos_x + CELL_SIZE, pos_y + CELL_SIZE * 0.75),
                (pos_x + CELL_SIZE * 0.5, pos_y + CELL_SIZE),
                (pos_x, pos_y + CELL_SIZE * 0.75),
                (pos_x, pos_y + CELL_SIZE * 0.25)
            ])

    # Update the screen
    pygame.display.flip()

# Quit the Pygame module
pygame.quit()