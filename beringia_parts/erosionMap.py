import numpy as np
import pygame

# Set the size of the grid and number of iterations
size = 50
iterations = 200

# Set the size of each cell in pixels
cell_size = 10

# Set the erosion parameters
erosion_rate = 0.1
deposition_rate = 0.05
min_slope = 0.1

# Initialize Pygame
pygame.init()

# Set the screen dimensions based on the grid size and cell size
screen_width = size * cell_size
screen_height = size * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))

# Generate a random grid of elevations
grid = np.random.rand(size, size)

# Main simulation loop
running = True
while running:
    for i in range(iterations):
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Calculate the slope of each cell
        gradient_x, gradient_y = np.gradient(grid)
        slope = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
        
        # Calculate the erosion and deposition for each cell
        erosion = slope * erosion_rate
        deposition = slope * deposition_rate
        
        # Determine the direction of the erosion and deposition
        erosion_direction = np.gradient(grid - erosion, axis=0)[1] < 0
        deposition_direction = np.gradient(grid + deposition, axis=0)[1] > 0
        
        # Update the grid based on the erosion and deposition
        grid = grid - erosion_direction * erosion + deposition_direction * deposition
        
        # Constrain the elevations to be between 0 and 1
        grid = np.clip(grid, 0, 1)
        
        # Clear the screen
        screen.fill((255, 255, 255))
        
        # Draw the grid
        for y in range(size):
            for x in range(size):
                color = (int(grid[y][x] * 255), int(grid[y][x] * 255), int(grid[y][x] * 255))
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)
        
        # Update the display
        pygame.display.update()
    
    # Wait for user input to quit the program
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

# Quit Pygame
pygame.quit()