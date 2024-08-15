import pygame
import sys
import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 50
WIDTH = 10
HEIGHT = 10
SCREEN_SIZE = (WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game objects
WALL = '#'
PLAYER = '@'
BOX = '$'
EMPTY_TARGET = '.'
FILLED_TARGET = '*'
PLAYER_ON_TARGET = '+'
FLOOR = ' '

# Level layout
level = [
    "########",
    "# $.####",
    "#  ..  #",
    "#  ##$ #",
    "##     #",
    "##$  ###",
    "##@  ###",
    "########"
]
# level = [
#     "########",
#     "#      #",
#     "# $  . #",
#     "# $  . #",
#     "# $  . #",
#     "#      #",
#     "# @    #",
#     "########"
# ]

# Create the game window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Sokoban")

# Find the player's starting position
player_pos = None
for y, row in enumerate(level):
    for x, cell in enumerate(row):
        if cell == PLAYER:
            player_pos = [x, y]
            break
    if player_pos:
        break

def draw_level():
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell == WALL:
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == BOX:
                pygame.draw.rect(screen, RED, rect)
            elif cell == EMPTY_TARGET:
                pygame.draw.rect(screen, GREEN, rect)
            elif cell == FILLED_TARGET:
                pygame.draw.rect(screen, RED, rect.inflate(-10, -10))
            elif cell == PLAYER_ON_TARGET:
                pygame.draw.rect(screen, BLUE, rect.inflate(-10, -10))
            elif cell == PLAYER:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def move_player(dx, dy):
    global player_pos
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    
    if level[new_y][new_x] == WALL:
        return
    
    if level[new_y][new_x] in (BOX, FILLED_TARGET):
        box_new_x, box_new_y = new_x + dx, new_y + dy
        if level[box_new_y][box_new_x] in (WALL, BOX, FILLED_TARGET):
            return
        
        # Move the box
        if level[box_new_y][box_new_x] == EMPTY_TARGET:
            level[box_new_y] = level[box_new_y][:box_new_x] + FILLED_TARGET + level[box_new_y][box_new_x+1:]
        else:
            level[box_new_y] = level[box_new_y][:box_new_x] + BOX + level[box_new_y][box_new_x+1:]
        
        if level[new_y][new_x] == FILLED_TARGET:
            level[new_y] = level[new_y][:new_x] + EMPTY_TARGET + level[new_y][new_x+1:]
        else:
            level[new_y] = level[new_y][:new_x] + FLOOR + level[new_y][new_x+1:]
    
    # Move the player
    current_cell = level[player_pos[1]][player_pos[0]]
    if current_cell == PLAYER:
        level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + FLOOR + level[player_pos[1]][player_pos[0]+1:]
    elif current_cell in (PLAYER_ON_TARGET, EMPTY_TARGET, FILLED_TARGET):
        level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + EMPTY_TARGET + level[player_pos[1]][player_pos[0]+1:]
    
    new_cell = level[new_y][new_x]
    if new_cell == EMPTY_TARGET:
        level[new_y] = level[new_y][:new_x] + PLAYER_ON_TARGET + level[new_y][new_x+1:]
    else:
        level[new_y] = level[new_y][:new_x] + PLAYER + level[new_y][new_x+1:]
    
    player_pos = [new_x, new_y]

def check_win():
    for row in level:
        if BOX in row or EMPTY_TARGET in row or PLAYER_ON_TARGET in row:
            return False
    return True


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_player(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)
    
    screen.fill(WHITE)
    draw_level()
    pygame.display.flip()
    
    if check_win():
        print("Congratulations! You won!")
        running = False

pygame.quit()
sys.exit()
