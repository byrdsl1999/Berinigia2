import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Set up grid size and initial elevation values
grid_size = 100
elevation = np.zeros((grid_size, grid_size))
elevation[grid_size//2, grid_size//2] = 1

# Set up velocity vectors for each cell
velocity_x = np.zeros((grid_size, grid_size))
velocity_y = np.zeros((grid_size, grid_size))

# Set up parameters for tectonic plate movement
plate_speed = 0.001
plate_divergence = 0.1
plate_convergence = 0.05

# Set up erosion parameters
erosion_rate = 0.01
rainfall = np.ones((grid_size, grid_size))

# Set up volcanic activity parameters
volcano_frequency = 0.001
volcano_eruption_size = 0.1

# Create figure and axes for the plot and slider
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
elev_map = ax.imshow(elevation, cmap='terrain')
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Time Step', 0, 99, valinit=0, valstep=1)

# Function to update the plot when the slider is changed
def update(val):
    t = int(slider.val)
    # Update velocity vectors based on plate movement
    velocity_x += plate_speed * (np.roll(elevation, 1, axis=1) - np.roll(elevation, -1, axis=1)) / 2
    velocity_y += plate_speed * (np.roll(elevation, 1, axis=0) - np.roll(elevation, -1, axis=0)) / 2
    
    # Update elevation based on velocity vectors
    elevation += velocity_x + velocity_y
    
    # Add volcanic eruptions
    volcano_locations = np.random.rand(grid_size, grid_size) < volcano_frequency
    elevation[volcano_locations] += np.random.rand(np.sum(volcano_locations)) * volcano_eruption_size
    
    # Add erosion
    elevation -= erosion_rate * rainfall * np.roll(elevation, 1, axis=0)
    
    # Add plate movement
    divergence_locations = np.random.rand(grid_size, grid_size) < plate_divergence
    convergence_locations = np.random.rand(grid_size, grid_size) < plate_convergence
    velocity_x[divergence_locations] += plate_speed
    velocity_x[convergence_locations] -= plate_speed
    velocity_y[divergence_locations] += plate_speed
    velocity_y[convergence_locations] -= plate_speed
    
    # Update the plot
    elev_map.set_data(elevation)
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
