from game.scripts.Constants import *
from game.scripts.Game import Game
from game.scripts.gui.Square import Square
from game.scripts.logic.Move import Move

import sys
import pygame

class Main:
    
    def __init__(self):
        pygame.init()                                              
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))     
        pygame.display.set_caption("Chess")                         

        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
        
        self.game = Game(self.game_surface)  

    def run(self):  
        _game_surface = self.game_surface
        _menu_surface = self.menu_surface
        _surface = self.surface
        _game = self.game
        _board = _game.board
        _drag = _game.drag
        
        FONT = pygame.font.Font(None, 32)  

        def display():
            _game.display_board()
            _game.display_last_move()
            _game.display_moves()
            _game.display_pieces()

        while True:
            _game.update_timer()  

            _menu_surface.fill((255, 255, 255))  

            display()  
            
            _surface.blit(_game_surface, (0, 0))
            _surface.blit(_menu_surface, (GAME_WIDTH, 0))

            p1_time_text = FONT.render(
                f"White: { _game.player_times[0] // 60}:{_game.player_times[0] % 60:02d}",
                True, (0, 0, 0)
            )
            _surface.blit(p1_time_text, (GAME_WIDTH + 20, 50))

            p2_time_text = FONT.render(
                f"Black: { _game.player_times[1] // 60}:{_game.player_times[1] % 60:02d}",
                True, (0, 0, 0)
            )
            _surface.blit(p2_time_text, (GAME_WIDTH + 20, 100))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    _drag.update_pos(event.pos)
                    clicked_row = _drag.mouse_y // SQUARE_SIZE
                    clicked_col = _drag.mouse_x // SQUARE_SIZE
                    
                    if Square.in_range(clicked_row, clicked_col):
                        if _board.squares[clicked_row][clicked_col].has_piece():
                            piece = _board.squares[clicked_row][clicked_col].piece
                            if piece.color == _game.next_turn_player:
                                _board.calc_moves(piece, clicked_row, clicked_col)
                                _drag.initial_pos(event.pos)
                                _drag.drag_set(piece)
                                display()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if _drag.dragging:
                        _drag.update_pos(event.pos)
                        final_row = _drag.mouse_y // SQUARE_SIZE
                        final_col = _drag.mouse_x // SQUARE_SIZE

                        initial = Square(_drag.initial_row, _drag.initial_col)
                        final = Square(final_row, final_col)
                        move = Move(initial, final)

                        if _board.valid_move(_drag.piece, move):
                            captured = _board.squares[final_row][final_col].has_piece()
                            _board.final_move(_drag.piece, move)
                            _game.move_capture_sound(captured)

                            _game.start_timer()  
                            _game.next_turn()  

                            display()
                        else:
                            _game.illegal_sound()
                        
                        _drag.undrag_set()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
