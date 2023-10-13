import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

TERRAIN_COLORS = {
	0: (255, 255, 255), # white
	1: (0, 0, 128),   # dark blue
	2: (0, 0, 255),   # blue
	3: (0, 128, 255), # light blue
	4: (0, 255, 255), # cyan
	5: (128, 255, 128), # light green
	6: (0, 255, 0),   # green
	7: (128, 128, 0), # olive
	8: (255, 255, 0), # yellow
	9: (255, 128, 0), # orange
	10: (255, 0, 0)   # red
}

# Set the dimensions of the grid
CELL_SIZE = 50
NUM_ROWS = 10
NUM_COLS = 10
GRID_WIDTH = CELL_SIZE * NUM_COLS
GRID_HEIGHT = CELL_SIZE * NUM_ROWS

# Set the size of the Pygame window
WINDOW_WIDTH = GRID_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT + 50
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Define the size and position of the reset button
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_X = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
BUTTON_Y = WINDOW_HEIGHT - BUTTON_HEIGHT - 20

class Cell:
    def __init__(self, row, col, color=WHITE, value=0):
        self.row = row
        self.col = col
        self.color = color
        self.value = value

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.col*CELL_SIZE, self.row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (self.col*CELL_SIZE, self.row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def handle_click(self, pos):
        if reset_button_rect.collidepoint(pos):
            reset_board()
        elif self.row < NUM_ROWS and self.col < NUM_COLS:
            current_color_index = self.value
            next_color_index = (current_color_index + 1) % len(TERRAIN_COLORS)
            self.value = next_color_index
            self.color = TERRAIN_COLORS[self.value]


# Define the function to draw the grid
def draw_grid():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            #pygame.draw.rect(screen, TERRAIN_COLORS[grid[row][col]], (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, grid2[row][col].color, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Define the function to handle mouse clicks
def handle_click(pos):
    col = pos[0] // CELL_SIZE
    row = pos[1] // CELL_SIZE
    print("Click at pos: " + str(pos))
    # Check if the user clicked on the reset button
    if reset_button_rect.collidepoint(pos):
        reset_board()
    elif row < NUM_ROWS and col < NUM_COLS:
        # Get the current color index for this cell
        # current_color_index = grid[row][col]
        current_color_index = grid2[row][col].value

        print(current_color_index)
        # Cycle to the next color index (wrapping around if necessary)
        next_color_index = (current_color_index + 1) % len(TERRAIN_COLORS)
        # Set the new color for this cell
        grid2[row][col].value = next_color_index
        grid2[row][col].color = TERRAIN_COLORS[next_color_index]

# Define the function to reset the grid
def reset_board():
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            eachCellColorKey = random.randint(0,10)
            grid[i][j] = eachCellColorKey
            
            grid2[i][j] = Cell(i, j, color = TERRAIN_COLORS[eachCellColorKey], value = eachCellColorKey)

# Initialize Pygame
pygame.init()

# Set the title of the Pygame window
pygame.display.set_caption("Click on cells to change color")

# Create a 2D list to store the cell colors
print(str(NUM_COLS) + "  " + str(NUM_ROWS))
grid = [[0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
print(str(NUM_COLS) + "  " + str(NUM_ROWS))
grid2 = [[Cell(row, col) for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
print(grid2)


# Create a Rect object for the reset button
reset_button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

# Create a font object to display text
font = pygame.font.Font(None, 36)

# Create a button object for the reset button
reset_button = pygame.Rect(GRID_WIDTH // 4, GRID_HEIGHT + 10, GRID_WIDTH // 2, 30)

# Run the Pygame loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			handle_click(pos)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				reset_board()

	# Clear the screen
	screen.fill(WHITE)

	# Draw the grid
	draw_grid()

	# Draw the reset button

	pygame.draw.rect(screen, GRAY, reset_button)
	reset_text = font.render("Reset", True, WHITE)
	reset_text_rect = reset_text.get_rect(center=reset_button.center)
	screen.blit(reset_text, reset_text_rect)

	# Update the screen
	pygame.display.flip()

# Quit Pygame
pygame.quit()