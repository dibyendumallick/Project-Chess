from game.scripts.Constants import *
from game.scripts.gui.Square import Square
from game.scripts.gui.Piece import *
from game.scripts.logic.Move import Move
from game.scripts.config.Config import Config

import pygame

class Board:
    
    #initialize board with double dimensional square list
    def __init__(self):
        #a list of rows, each being a list of Square objects
        self.squares = [[Square(row, col) for row in range(ROWS)] for col in range(COLS)] #each square becomes an object
        self.last_move = None           #last move made on the board
        self._add_piece('white')        #adds pieces with white color
        self._add_piece('black')        #adds pieces with black color
        self.config = Config()          #Config object
    
    #add piece of a color to any square of the board
    def _add_piece(self, color):
        row_pawn, row_king = (6, 7) if color == 'white' else (1, 0)         #rows for pawns and king
        
        #Pawn Placement
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        #Rook Placement
        self.squares[row_king][0] = Square(row_king, 0, Rook(color))
        self.squares[row_king][7] = Square(row_king, 7, Rook(color))
        
        #Knight Placement
        self.squares[row_king][1] = Square(row_king, 1, Knight(color))
        self.squares[row_king][6] = Square(row_king, 6, Knight(color))
        
        #Bishop Placement
        self.squares[row_king][2] = Square(row_king, 2, Bishop(color))
        self.squares[row_king][5] = Square(row_king, 5, Bishop(color))
        
        #Queen Placement
        self.squares[row_king][3] = Square(row_king, 3, Queen(color))
        
        #King Placement
        self.squares[row_king][4] = Square(row_king, 4, King(color))
    
    #method to change the board attributes if a move is made
    def final_move(self, piece, move):
        initial = move.initial          #initial Square of move
        final = move.final              #final Square of move
        
        #game board piece update
        self.squares[initial.row][initial.col].piece = None         #initial Square piece set to None
        self.squares[final.row][final.col].piece = piece            #final Square piece set to actual piece
        
        #pawn promotion
        if isinstance(piece, Pawn):
            self.promotion(piece, final)            #calls method to promote Pawn piece at final Square
        
        #castling
        if isinstance(piece, King):
            if abs(initial.col - final.col) == 2:                                   #if King moves 2 squares
                difference = final.col - initial.col                                #difference between final and initial col
                rook = piece.left_rook if difference < 0 else piece.right_rook      #left rook if king moves to left, else right rook
                if isinstance(rook, Rook):                                          #if rook belongs to Rook class
                    self.config.castle_sound.play()                                 #play castling sound
                    self.final_move(rook, rook.moves[-1])                           #move rook as per the last move in its moves list
        
        #move set to true
        piece.moved = True
        piece.first_move = True
        #clear list of valid moves since no more valid moves are possible until next turn
        piece.clear_moves()
        #set last move to true (for rendering purposes)
        self.last_move = move
        
        #debug print, prints the move made
        print(f'{piece.color} {piece.name} moved from {chr(initial.col+97)}{ROWS-initial.row} to {chr(final.col+97)}{ROWS-final.row}')
    
    #method to check if a move is in valid moves list of piece
    def valid_move(self, piece, move):
        return move in piece.moves
    
    #method to check if a move puts the king in check
    def in_check(self, piece, move):
        pass
    
    #method to promote a Pawn to a queen
    def promotion(self, piece, final):
        if final.row == 0 or final.row == 7:                                    #checks if pawn has reached 0th or 7th row
            self.config.promote_sound.play()                                    #plays promotion sound
            self.squares[final.row][final.col].piece = Queen(piece.color)       #renders a Queen piece at final Square
    
    #defining castling move squares of rooks and king 
    def castle_moves(self, king, rook, rook_col):
        row = 0 if king.color == 'black' else 7                                 #sets row number as per piece's color
        
        #left col and right define columns to check for pieces obstructing castling
        left_col = 1 if rook_col == 0 else 5                                    #sets left column number as per rook's column
        right_col = 4 if rook_col == 0 else 7                                   #sets right column number as per rook's column
        while left_col < right_col:                                             #iterates from left col(inclusive) to right col(exclusive)
                if self.squares[row][left_col].has_piece():                     #a piece is blocking the castle
                    break
                left_col += 1
                                
        if left_col == right_col:                                               #if the iterator i has verified no obstructions upto right col
            king.left_rook = rook if rook_col == 0 else None                    #left rook set to rook if rook_col is 0, else None
            king.right_rook = rook if rook_col == 7 else None                   #right rook set to rook if rook_col is 7, else None
                                    
            #rook move
            initial = Square(row, rook_col)                                     #initial Square for rook
            final = Square(row, 3) if rook_col == 0 else Square(row, 5)         #final Square for rook, col = 3 or 5 depending on rook
            move = Move(initial, final)                                         #Move object for rook
            rook.add_move(move)                                                 #adds the move to valid moves list of rook
                                    
            #king move 
            initial = Square(row, 4)                                            #initial Square for king
            final = Square(row, 2) if rook_col == 0 else Square(row, 6)         #final Square for king, col = 2 or 6 depending on rook
            move = Move(initial, final)                                         #Move object for king
            king.add_move(move)                                                 #adds the move to valid moves list of king
    
    #Calculate valid moves for each piece
    def calc_moves(self, piece, row, col):
        
        #moves calculation for pawns
        def pawn_moves():
            #steps for pawn piece
            steps = 1 if piece.first_move else 2
            
            #forward, no capture
            start = row + piece.direction                                   #start row for pawn
            end = row + (piece.direction * (1 + steps))                     #end row for pawn
            for possible_move_row in range(start, end, piece.direction):    #iterates from start to end row in direction of piece
                if Square.in_range(possible_move_row):                      #if possible_move_row is within range(0 to 7)
                    if self.squares[possible_move_row][col].is_empty():     #if the square is empty
                        initial = Square(row, col)                          #initial Square for move
                        final = Square(possible_move_row, col)              #final Square for move
                        move = Move(initial, final)                         #Move object for pawn
                        piece.add_move(move)                                #adds the move to valid moves list of pawn
                    else:
                        break                                               #blocked by piece
                else:
                    break                                                   #out of range
            
            #diagonal, to capture
            possible_move_row = row + piece.direction                       #final row for pawn
            possible_move_cols = [col-1, col+1]                             #left or right col for pawn
            for possible_move_col in possible_move_cols:                    #iterates over left and right col
                if Square.in_range(possible_move_row, possible_move_col):   #if possible_move_row and possible_move_col are within range(0 to 7)
                    if self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):   #if the square has enemy piece
                        initial = Square(row, col)                          #initial Square for move
                        final_piece = self.squares[possible_move_row][possible_move_col].piece      #enemy piece
                        final = Square(possible_move_row, possible_move_col, final_piece)           #final Square for move
                        move = Move(initial, final)                         #Move object for pawn
                        piece.add_move(move)                                #adds the move to valid moves list of pawn
        
        #moves calculation for knights and kings
        def fixed_step_moves(possible_moves):
            
            for possible_move in possible_moves:                                    #iterates through all moves in given list of moves
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):           #if possible row and col are within range(0 to 7)
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        
                        #create initial and final Square objects
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        #create move and add to valid moves list
                        move = Move(initial, final)
                        piece.add_move(move)
                
            #Castling        
            if isinstance(piece, King):
                if not piece.first_move:                                        #if piece has not moved yet
                    left_rook = self.squares[row][0].piece                      #assigns left rook
                    right_rook = self.squares[row][7].piece                     #assigns right rook

                    #queen-side castling
                    if isinstance(left_rook, Rook):
                        if not left_rook.first_move:
                            self.castle_moves(piece, left_rook, 0)              #castles with rook_col = 0 if rook hasn't moved yet       
                    #king-side castling
                    if isinstance(right_rook, Rook):
                        if not right_rook.first_move:
                            self.castle_moves(piece, right_rook, 7)             #castles with rook_col = 7 if rook hasn't moved yet
        
        #moves calculation for bishops, rooks, and queens
        def variable_step_moves(possible_moves):
            
            for possible_move in possible_moves:
                row_line, col_line = possible_move
                possible_move_row = row + row_line
                possible_move_col = col + col_line
                
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        
                        #create initial and final Square objects
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        #create move
                        move = Move(initial, final)
                        
                        #add move to valid moves list if Square is empty, and continue the loop
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)
                        
                        #break the loop if obstructed by team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                            break
                            
                        #break the loop if obstructed by enemy piece, but add move to valid moves list to capture the piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                            piece.add_move(move)
                            break
                    
                    #row and col are out of range        
                    else:
                        break
                    
                    possible_move_row += row_line       #increment row number using given increment
                    possible_move_col += col_line       #increment column number using given increment
        
        #calling moves calculation method for pawns
        if isinstance(piece, Pawn):
            pawn_moves()    
        
        #calling moves calculation method for knights
        elif isinstance(piece, Knight):
            fixed_step_moves([
                (row+2, col-1),         #down-left
                (row+2, col+1),         #down-right
                (row-2, col-1),         #up-left
                (row-2, col+1),         #up-right
                (row-1, col-2),         #left-up
                (row-1, col+2),         #right-up
                (row+1, col-2),         #left-down
                (row+1, col+2)          #right-down
            ])
        
        #calling moves calculation method for bishops
        elif isinstance(piece, Bishop):
            variable_step_moves([
                (-1, -1),               #up-left
                (-1, 1),                #up-right
                (1, -1),                #down-left
                (1, 1)                  #down-right
            ])  
        
        #calling moves calculation method for rooks
        elif isinstance(piece, Rook):
            variable_step_moves([
                (-1, 0),                #up
                (1, 0),                 #down
                (0, -1),                #left
                (0, 1)                  #right
            ])    
        
        #calling moves calculation method for queens
        elif isinstance(piece, Queen):
            variable_step_moves([
                (-1, -1),               #up-left
                (-1, 1),                #up-right
                (1, -1),                #down-left
                (1, 1),                 #down-right
                (-1, 0),                #up
                (1, 0),                 #down
                (0, -1),                #left
                (0, 1)                  #right
            ])    
        
        #calling moves calculation method for kings
        elif isinstance(piece, King):
            fixed_step_moves([
                (row+1, col),           #down
                (row+1, col+1),         #down-right
                (row+1, col-1),         #down-left
                (row-1, col),           #up
                (row-1, col+1),         #up-right
                (row-1, col-1),         #up-left
                (row, col-1),           #left
                (row, col+1)            #right
            ])