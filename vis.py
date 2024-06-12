import pygame
import json
from os import listdir
from time import sleep

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

FPS = 20
CELL_SIZE = 20
PADDING = 3 * CELL_SIZE
COLORS = [
    (41, 41, 41), # Gray16
    (235, 64, 52),  # Red Berry
    (249, 246, 246),  # Misty Rose
    (209, 204, 192),  # Gray Chateau
    (204, 209, 209),  # Pale Slate
    (153, 204, 204),  # Pale Cyan
    (102, 179, 179),  # Medium Turquoise
    (51, 153, 153),  # Dark Cyan
    (0, 128, 128),  # Teal
    (0, 102, 102)  # Dark Teal
]
LINE_COLOR = (170, 255, 24)
DOT_RADIUS = 5

task_files = listdir("./data/training")
print(f"Found {len(task_files)} Task JSON Files!")

# Code to load data from files
def load_file(file_index):
    with open(f'./data/training/{task_files[file_index]}') as f:
        print(f"Loading {task_files[file_index]}...")
        data = json.load(f)
        print("Complete!")
    return data

current_file = 0
data = load_file(current_file)

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    infoObject = pygame.display.Info()
    SCREEN_WIDTH = infoObject.current_w

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_file = current_file - 1  if current_file > 0 else len(task_files) - 1
                data = load_file(current_file)
            elif event.key == pygame.K_RIGHT:
                current_file = current_file + 1 if current_file < len(task_files) - 1 else 0
                data = load_file(current_file)

    screen.fill((255, 255, 255))

    input_origin_x, output_origin_x, grid_origin_y, max_height = PADDING, 0, PADDING, 0
    for example in data["train"]:
        input_grid = example['input']
        output_grid = example['output']

        grids_width = ((len(input_grid[0]) + len(output_grid[0])) * CELL_SIZE) + (2*PADDING)
        if input_origin_x + grids_width > SCREEN_WIDTH:
            input_origin_x = PADDING
            grid_origin_y += max_height + PADDING

        output_origin_x = input_origin_x + (len(input_grid[0]) * CELL_SIZE) + PADDING
        # update max_height if the current grid is taller
        grid_height = max(len(input_grid), len(output_grid)) * CELL_SIZE
        if grid_height > max_height:
            max_height = grid_height

        for i in range(len(input_grid[0])):
            for j in range(len(input_grid)):
                rect = pygame.Rect(input_origin_x + (i * CELL_SIZE), grid_origin_y + (j * CELL_SIZE), CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS[input_grid[j][i]], rect)

        for i in range(len(output_grid[0])):
            for j in range(len(output_grid)):
                rect = pygame.Rect(output_origin_x + (i * CELL_SIZE), grid_origin_y + (j * CELL_SIZE), CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLORS[output_grid[j][i]], rect)

        # Draw the line from center to center
        input_center = (input_origin_x + len(input_grid[0]) * CELL_SIZE // 2, grid_origin_y + len(input_grid) * CELL_SIZE // 2)
        output_center = (output_origin_x + len(output_grid[0]) * CELL_SIZE // 2, grid_origin_y + len(output_grid) * CELL_SIZE // 2)
        pygame.draw.line(screen, LINE_COLOR, input_center, output_center, 2)

        # Draw dots at each end of the line
        pygame.draw.circle(screen, LINE_COLOR, input_center, DOT_RADIUS)
        pygame.draw.circle(screen, LINE_COLOR, output_center, DOT_RADIUS)

        input_origin_x += grids_width

    pygame.display.flip()

pygame.quit()
