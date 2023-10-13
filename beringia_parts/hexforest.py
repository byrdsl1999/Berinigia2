import random
import pygame
import math

# Set up the game window
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 10
ROWS, COLS = math.ceil(HEIGHT / (CELL_SIZE * 1.5)), math.ceil(WIDTH / (CELL_SIZE * 2))  # calculate number of rows and cols
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Set up the initial state of the grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for row in range(ROWS):
    for col in range(COLS):
        if random.random() < 0.6:
            grid[row][col] = 1

# Define the game loop
while True:

    # Clear the screen
    screen.fill(BLACK)

    # Create a copy of the grid
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Iterate over each cell in the grid
    for row in range(ROWS):
        for col in range(COLS):

            # Check if the cell is a tree
            if grid[row][col] == 1:

                # Calculate the center of the hexagon
                x = CELL_SIZE * 2 * col + CELL_SIZE * (row % 2)
                y = CELL_SIZE * 1.5 * row

                # Draw the tree
                pygame.draw.polygon(screen, GREEN, [
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE/2, y + CELL_SIZE * math.sqrt(3) / 2),
                    (x - CELL_SIZE/2, y + CELL_SIZE * math.sqrt(3) / 2),
                    (x - CELL_SIZE, y),
                    (x - CELL_SIZE/2, y - CELL_SIZE * math.sqrt(3) / 2),
                    (x + CELL_SIZE/2, y - CELL_SIZE * math.sqrt(3) / 2)
                ])

                # Check if the tree catches fire
                if any(grid[i][j] == 2 for i in range(row-1, row+2) for j in range(col-1, col+2) if (i >= 0 and j >= 0 and i < ROWS and j < COLS)) or random.random() < 0.0001:
                    new_grid[row][col] = 2

                # Check if a new tree grows
                elif random.random() < 0.01:
                    new_grid[row][col] = 1

                # Otherwise, keep the tree
                else:
                    new_grid[row][col] = 1

            # Check if the cell is a burning tree
            elif grid[row][col] == 2:

                # Calculate the center of the hexagon
                x = CELL_SIZE * 2 * col + CELL_SIZE * (row % 2)
                y = CELL_SIZE * 1.5 * row

                # Draw the burning tree
                pygame.draw.polygon(screen, ORANGE, [
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE/2, y + CELL_SIZE * math.sqrt(3) / 