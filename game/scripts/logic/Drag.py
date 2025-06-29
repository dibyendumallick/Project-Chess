from game.scripts.Constants import *

import pygame

class Drag:
    
    def __init__(self):
        self.mouse_x = 0                #mouse coordinate for x-axis
        self.mouse_y = 0                #mouse coordinate for y-axis
        self.initial_row = 0            #initial row of piece being dragged
        self.initial_col = 0            #initial col of piece being dragged
        self.final_row = 0              #final row of piece being released
        self.final_col = 0              #final col of piece being released
        self.piece = None               #piece being dragged
        self.dragging = False           #drag state of Drag object
    
    #Blit method
    def update_blit(self, surface):
        image = pygame.image.load(self.piece.image)   #?                    #image to be rendered
        image_rect = (self.mouse_x, self.mouse_y)                           #position of square where image is to be rendered
        self.piece.image_rect = image.get_rect(center = image_rect)         #square where image is to be rendered
        surface.blit(image, self.piece.image_rect)                          #rendering image onto image_rect
    
    #Update methods
    #updating mouse coordinates
    def update_pos(self, pos):
        self.mouse_x, self.mouse_y = pos
        
    #initializing initial row and col from pos passed as parameter
    def initial_pos(self, pos):
        self.initial_row = pos[1] // SQUARE_SIZE    #pos[1] since pygame.event sets y value at pos[1], and y is required for row
        self.initial_col = pos[0] // SQUARE_SIZE    #pos[0] since pygame.event sets x value at pos[0], and x is required for col
        
    #initialize piece being dragged, and set Drag object's dragging state to true
    def drag_set(self, piece):
        self.piece = piece
        self.dragging = True
        
    #uninitialize released piece, and set Drag object's dragging state to false
    def undrag_set(self):
        self.piece = None
        self.dragging = False