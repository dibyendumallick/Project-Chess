from game.scripts.gui.Piece import *

class Square:
    
    def __init__(self, row, col, piece = None):
        self.row = row              #row of the Square object
        self.col = col              #col of the Square object
        self.piece = piece          #piece on the Square object
        
    #equating two Square objects 
    def __eq__(self, value):
        return self.row == value.row and self.col == value.col
    
    #method to check if Square object has ANY piece
    def has_piece(self):
        return self.piece != None
    
    #method to check if Square object has NO piece
    def is_empty(self):
        return not self.has_piece()
    
    #method to check if Square object has SAME COLOR piece
    def has_team(self, color):
        return self.has_piece() and self.piece.color == color
    
    #method to check if Square object has OPPOSITE COLOR piece
    def has_enemy(self, color):
        return self.has_piece() and self.piece.color != color

    #method to check if Square object has OPPOSITE COLOR or NO piece
    def is_empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy(color)
    
    #method to check if row, col (and any other given variables) are within range of the board, i.e., within 0 and 7
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True