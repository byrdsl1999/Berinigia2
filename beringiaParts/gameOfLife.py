import pygame
import numpy as np

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define constants
CELL_SIZE = 10
ROW_COUNT = 60
COLUMN_COUNT = 80
WIDTH = COLUMN_COUNT * CELL_SIZE
HEIGHT = ROW_COUNT * CELL_SIZE

# Initialize the pygame module
pygame.init()

# Set the size of the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption of the display window
pygame.display.set_caption("Conway's Game of Life")

# Create the initial state of the board
board = np.random.randint(2, size=(ROW_COUNT, COLUMN_COUNT))

# Define the game loop
while True:

    # Clear the screen
    screen.fill(BLACK)

    # Create a copy of the board
    new_board = board.copy()

    # Iterate over each cell in the board
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):

            # Count the number of neighbors
            neighbors = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0):
                        x = row + i
                        y = column + j
                        if x >= 0 and x < ROW_COUNT and y >= 0 and y < COLUMN_COUNT:
                            if board[x][y] == 1:
                                neighbors += 1

            # Apply the rules of the game
            if board[row][column] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_board[row][column] = 0
            else:
                if neighbors == 3:
                    new_board[row][column] = 1

            # Draw the cell
            if new_board[row][column] == 1:
                pygame.draw.rect(screen, WHITE, (column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the board
    board = new_board

    # Update the display
    pygame.display.update()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            