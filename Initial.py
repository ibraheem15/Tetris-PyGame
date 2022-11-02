from turtle import position
from numpy import place
import pygame
import random
import time
import datetime
import sys

pygame.font.init()

# Grid will be 10 x 20	

# Global Variables
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height


# Shape Formats

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
class DigitalClock(pygame.sprite.Sprite):
    def __init__(self, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.font = pygame.font.SysFont('Corbel', 30, bold=True)
        self.rect = pygame.Rect(location, (0, 0))  # placeholder
        self.update()

    def update(self):
        location = self.rect.left, self.rect.top  # save position
        time_text = datetime.datetime.now().strftime("%H:%M:%S")
        self.image = self.font.render(time_text, 1, [255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  # restore position

class Piece(object):
    # Constructor
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
    
def create_grid(locked_positions={}): # Locked Positions is a dictionary which will have the position of the blocks that are already placed
    grid = [[(0,0,0) for x in range(10)] for x in range(20)] # 2d list where each row (20) is a list of 10 values which are RGB values
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (col, row) in locked_positions:
                c = locked_positions[(col, row)]
                grid[row][col] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] # shape.shape is a list of the 4 different shapes, shape.rotation is the current rotation of the shape

    for count, line in enumerate(format): 
        # enumerate returns the index and the value of the list at that index # count is the index
        row = list(line) # list creates a list of the 4 different shapes or in c++ terms, an array of the 4 different shapes
        for count2, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + count2, shape.y + count)) 
                # shape.x and shape.y are the x and y coordinates of the shape on the grid
                # adding of count and count2 is to mpve the position of the shape on the grid
        
    for count, pos in enumerate(positions):
        positions[count] = (pos[0] - 2, pos[1] - 4) 
        # subtracting 2 from the x coordinate and 4 from the y coordinate is to make the shape appear left and up on the grid because the dots in the shape.shape list makes it off center        

    return positions
    
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] # 2d list of all the positions that are empty
    accepted_pos = [j for sub in accepted_pos for j in sub] # flattens the list of lists into a single list # simple words 2d array to 1d array #try using numpy to flatten the list

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: # as we want the shape to drop from above the screen so checking if the y coordinate is greater than -1
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos # x and y are the x and y coordinates of the shape on the grid
        if y < 1: # if the y coordinate is less than 1 then the shape has reached the top of the screen and the game is lost
            return True
    return False # if the shape has not reached the top of the screen then the game is not lost

def get_shape():	
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface,grid):   
    for row in range(len(grid)):
        pygame.draw.line(surface,
                         (128,128,128), # Color
                         (top_left_x, top_left_y + row * block_size), # Start Position
                         (top_left_x + play_width, top_left_y + row * block_size) # End Position
                        )
        for col in range(len(grid[row])):
            pygame.draw.line(surface, (128,128,128),
                             (top_left_x + col * 30, top_left_y),
                             (top_left_x + col * 30, top_left_y + play_height)
                            )
                             
            

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1): # loop through the grid from the bottom to the top
        row = grid[i]
        if (0,0,0) not in row: # if the row is not empty or there is no black color in the row
            inc += 1
            ind = i
            for j in range(len(row)):
                try: # try to delete the row from the locked dictionary OR do the following code and if it fails then do the except code
                    del locked[(j,i)]
                except: # if the row is not in the locked dictionary then follow the code below
                    continue # if the position is not in the locked dictionary then continue
                
    # if the row is full then clear and shift all the rows above it down by 1
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1] )[::-1]: # sort the locked dictionary by the y coordinate of the position
            x, y = key #getting the x and y coordinates of the position
            if y < ind: # if the y coordinate of the position is less than the index of the row that was cleared
                newKey = (x, y+inc) # then create a new key with the same x coordinate and y coordinate + 1
                locked[newKey] = locked.pop(key) # pop the key and add it to the new key 
                
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Corbel', 30)
    label = font.render('Next Shape', 1, (255,255,255))
    
    place_location = ((top_left_x + play_width + 50), top_left_y + play_height/2 - 100) # location of the next shape
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for count, line in enumerate(format):
        row = list(line)
        for count2, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface,
                                 shape.color,
                                 (place_location[0] + count2 * block_size, place_location[1] + count * block_size, block_size, block_size), # 
                                 0
                                )
                
    surface.blit(label, (place_location[0] + 10, place_location[1] - 30)) # blit is used to draw the label on the surface
    
    

def draw_window(surface, grid,my_digital_clock,score=0):
    surface.fill((0,0,0)) # Fill the screen with black
    
    # Score
    score_font = pygame.font.SysFont('Corbel', 30, True)
    score_label = score_font.render('Score: ' + str(score), 1, (255,255,255))
    
    surface.blit(score_label, (top_left_x + play_width + 65, top_left_y + play_height/13 - 100)) # blit is used to draw the label on the surface
    
    pygame.font.init()
    font = pygame.font.SysFont('Corbel', 60)
    label = font.render('Tetris', 1, (255,255,255)) # Render the text
    
    surface.blit(label, (top_left_x + play_width / 2 # Get the width of the text and divide it by 2 to get the middle
                        - (label.get_width() / 2), 30
                        )) # Blit the text to the screen
    
    surface.blit(my_digital_clock.image, my_digital_clock.rect) # Blit the clock to the screen
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface,
                             grid[row][col],
                             (top_left_x + col * block_size, top_left_y + row * block_size, block_size, block_size), # Position and Size
                             0 # Thickness of the rectangle
                            )
    
    pygame.draw.rect(surface,
                     (255,0,0), # Red
                     (top_left_x, top_left_y, play_width, play_height), 
                     5 # Border width
                    )
        
    draw_grid(surface, grid) # Draw the grid
    # pygame.display.update() # Update the display
    

def main(win):
    locked_positions = {} # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.22
    fall_speed_increase = 0.005
    level_time = 0
    score = 0
    
    
    my_digital_clock = DigitalClock([1, 1], [50, 50]) # Create the clock
    TICK_EVENT = pygame.USEREVENT + 1 # create a new event type
    pygame.time.set_timer(TICK_EVENT, 1000)  # periodically create TICK_EVENT

    while run:
        grid = create_grid(locked_positions)
        fall_time += fall_clock.get_rawtime()
        level_time += fall_clock.get_rawtime()
        fall_clock.tick()
        
        if level_time/1000 > 5: # if the level time is greater than 5 seconds then increase the fall speed
            level_time = 0
            if fall_speed - fall_speed_increase > 0.12:
                fall_speed -= fall_speed_increase
                
        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0: 
                # if the shape is not in a valid space and the y coordinate is greater than 0 
                # then the shape has reached the bottom of the screen
                current_piece.y -= 1 # move the shape up by 1
                change_piece = True # change the shape to the next shape and lock the current shape in place
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.font.quit()
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
            
            if event.type == TICK_EVENT:
                my_digital_clock.update()  # call new method
            
        shape_pos = convert_shape_format(current_piece)
        
        #color the shape 
        for i in range(len(shape_pos)):
            x, y = shape_pos[i] 
            if y > -1: # if the y coordinate is greater than -1 then the shape is on the grid
                grid[y][x] = current_piece.color # color the shape
                 
        if change_piece: #w if the shape has reached the bottom of the screen
            for pos in shape_pos: 
                p = (pos[0], pos[1]) # p is the position of the shape on the grid
                locked_positions[p] = current_piece.color 
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10 # add 10 points for each row cleared
       
        draw_window(win, grid, my_digital_clock,score) # draw the window with the grid and the clock
        draw_next_shape(next_piece, win) # draw the next shape
        pygame.display.update()
        
        if check_lost(locked_positions):
            run = False
                
        clock.tick(60)  # limit framerate
        pygame.display.flip()  
                                

def main_menu(win):
    main(win)

win = pygame.display.set_mode((screen_width, screen_height)) # Create the window
pygame.display.set_caption('Tetris') # Set the title of the window
main_menu(win)  # start game     