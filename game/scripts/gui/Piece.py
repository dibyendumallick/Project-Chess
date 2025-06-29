import os

class Piece:
    
    def __init__(self, name, color, value, image = None, image_rect = None):
        self.name = name                                #name of the piece
        self.color = color                              #color of the piece
        value_sign = 1 if color == 'white' else -1      #setting different signed values for different colors
        self.value = value * value_sign                 #setting different values for different pieces
        self.image = image                              #image of the piece to be rendered
        self.set_image()                                #setting the image to be rendered
        self.image_rect = image_rect                    #square on which the image is to be rendered
        self.moves = []                                 #list of valid moves for the piece
        self.moved = False                              #boolean flag to check if piece has moved in current turn
        self.first_move = False                         #boolean flag to check if piece has moved at all, used in castling
    
    #method to set image to be rendered for the piece    
    def set_image(self):
        #get the absolute path to the assets folder
        base_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/images"))

        #construct the full path to the piece image
        self.image = os.path.join(base_image_path, f"{self.color}_{self.name}.png")
    
    #add a valid Move object to list of valid moves    
    def add_move(self, move):
        self.moves.append(move)
        
    #clear the entire valid move list after the piece is moved
    def clear_moves(self):
        self.moves = []

#Classes to initialize piece objects with name, color, and value
class Pawn(Piece):
    
    def __init__(self, color):
        
        #initialize direction for pawns, since pawns can move in one direction only
        self.direction = -1 if color == 'white' else 1
        
        super().__init__('pawn', color, 1.0)
        
class Knight(Piece):
    
    def __init__(self, color):
        super().__init__('knight', color, 3.0)
       
class Bishop(Piece):
    
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)
        
class Rook(Piece):
    
    def __init__(self, color):
        super().__init__('rook', color, 5.0)
        
class Queen(Piece):
    
    def __init__(self, color):
        super().__init__('queen', color, 9.0)
        
class King(Piece):
    
    def __init__(self, color):
        self.left_rook = None           #initialize left rook for queen side castling
        self.right_rook = None          #initialize right rook for king side castling
        super().__init__('king', color, 1000.0) 