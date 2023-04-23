import numpy as np
import pygame
from moviepy.editor import ImageSequenceClip
import os

# define the grid size
grid_size = (100, 100)

# define the colors
bg_color = (230, 230, 250)
dead_color = (0, 0, 0)
alive_color = (230, 180, 230)

# initialize the grid with random values
grid = np.random.randint(2, size=grid_size)

# initialize pygame
pygame.init()

# set the window size and caption
window_size = (600, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Conway\'s Game of Life')

# define the cell size
cell_size = (window_size[0] // grid_size[0], window_size[1] // grid_size[1])

# create a list to store the frames
frames = []

# run the game loop
running = True
iteration = 0
while running and iteration < 200:
    # iterate over each cell in the grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the grid according to the rules of Conway's Game of Life
    new_grid = np.zeros(grid_size, dtype=int)
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            # count the number of live neighbors
            neighbors = np.sum(grid[max(0, i-1):min(grid_size[0], i+2), max(0, j-1):min(grid_size[1], j+2)]) - grid[i, j]
            # apply the rules of Conway's Game of Life
            if grid[i, j] == 1 and (neighbors == 2 or neighbors == 3):
                new_grid[i, j] = 1
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1

    # update the grid
    grid = new_grid

    # clear the screen
    screen.fill(bg_color)

    # draw the cells
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            color = alive_color if grid[i, j] else dead_color
            pygame.draw.rect(screen, color, (i*cell_size[0], j*cell_size[1], cell_size[0], cell_size[1]))

    # update the display
    pygame.display.flip()

    # add the current frame to the list
    surf = pygame.surfarray.make_surface(np.transpose(np.array(pygame.surfarray.array3d(screen)), (1, 0, 2)))
    surf_arr = np.array(pygame.surfarray.array3d(surf))
    frames.append(surf_arr)

    # print the current iteration
    print('Iteration:', iteration)

    # increment the iteration counter
    iteration += 1

# Create the GIF
clip = ImageSequenceClip(frames, fps=10)
clip.write_gif('game_of_life.gif')