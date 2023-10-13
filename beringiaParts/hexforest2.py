import pygame
import numpy as np

# Set grid size and cell size
size = 50
cell_size = 12

# Set window size
width = size * cell_size
height = int(size * cell_size * 0.87)
screen = pygame.display.set_mode((width, height))

# Set colors
colors = {
    0: (10, 100, 10),  # Tree
    1: (250, 100, 10),  # Fire
    2: (230, 230, 230)  # Burned tree
}

# Initialize grid with all trees
grid = np.zeros((size, size), dtype=np.int8)

# Set some trees on fire
grid[size//2, size//2] = 1

# Define probability of ignition and burning out for trees
p_ignition = 0.05
p_burnout = 0.01

# Define hexagonal neighbors
neighbors = [(-1, 0), (1, 0), (-1, 1), (0, 1), (1, -1), (0, -1)]

# Define function to calculate the next state of the grid
def next_state(grid):
    new_grid = np.copy(grid)
    for i in range(size):
        for j in range(size):
            # If the cell is a tree
            if grid[i,j] == 0:
                # Check if any neighboring cell is on fire
                for dx, dy in neighbors:
                    if (i+dx >= 0 and i+dx < size and j+dy >= 0 and j+dy < size):
                        if grid[i+dx,j+dy] == 1:
                            # Ignite tree with probability p_ignition
                            if np.random.random() < p_ignition:
                                new_grid[i,j] = 1
                                break
            # If the cell is on fire
            elif grid[i,j] == 1:
                # Burn out with probability p_burnout
                if np.random.random() < p_burnout:
                    new_grid[i,j] = 2
                else:
                    # Spread fire to neighboring trees
                    for dx, dy in neighbors:
                        if (i+dx >= 0 and i+dx < size and j+dy >= 0 and j+dy < size):
                            if grid[i+dx,j+dy] == 0:
                                new_grid[i+dx,j+dy] = 1
    return new_grid

# Define function to draw grid
def draw_grid(grid):
    for i in range(size):
        for j in range(size):
            color = colors[grid[i,j]]
            x = j * cell_size + (i%2) * cell_size//2
            y = i * cell_size * 0.87
            pygame.draw.polygon(screen, color, [(x, y+cell_size//2), (x+cell_size//2, y), (x+cell_size, y+cell_size//2), (x+cell_size//2, y+cell_size)])

# Run simulation
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(10)  # Limit frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))  # Clear screen
    draw_grid(grid)  # Draw grid
    pygame.display.flip()  # Update screen
    grid