import pygame
from game.scripts.Constants import *
from game.scripts.gui.Board import Board
from game.scripts.logic.Drag import Drag
from game.scripts.config.Config import Config

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.next_turn_player = 'white'
        self.board = Board()
        self.drag = Drag()
        self.config = Config()
        self.config.game_start_sound.play()

        # Timer Variables
        self.player_times = [600, 600]  # 10 minutes (600 seconds) for each player
        self.current_player = 0  # 0 = White, 1 = Black
        self.last_tick = None  # Timer starts tracking only after a move

    def start_timer(self):
        """ Starts the timer countdown only after a move is made """
        if self.last_tick is None:  
            self.last_tick = pygame.time.get_ticks()  # Start tracking time

    def update_timer(self):
        """ Updates the timer every second after a move is made """
        if self.last_tick is not None:
            now = pygame.time.get_ticks()
            if now - self.last_tick >= 1000:  # If 1 second has passed
                self.player_times[self.current_player] -= 1
                self.last_tick = now  

                # End the game if a player's time runs out
                if self.player_times[self.current_player] <= 0:
                    print(f"{'White' if self.current_player == 0 else 'Black'} ran out of time! Game over.")
                    self.last_tick = None  # Stop the timer

    def next_turn(self):
        """ Switches the turn when a move is made (not on Enter press) """
        self.next_turn_player = 'black' if self.next_turn_player == 'white' else 'white'
        self.current_player = 1 - self.current_player  # Swap players (0 → 1 or 1 → 0)
        self.last_tick = pygame.time.get_ticks()  # Reset timer tracking

    def draw_rect(self, scheme, row, col):
        color = scheme.light if (row + col) % 2 == 0 else scheme.dark
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(self.surface, color, rect)

    def display_board(self):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                self.draw_rect(theme.bg, row, col)

    def display_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.drag.piece:
                        image = pygame.image.load(piece.image)
                        image_rect = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.image_rect = image.get_rect(center=image_rect)
                        self.surface.blit(image, piece.image_rect)

    def display_moves(self):
        theme = self.config.theme
        if self.drag.dragging:
            piece = self.drag.piece
            for move in piece.moves:
                if self.board.squares[move.final.row][move.final.col].has_enemy(piece.color):
                    self.draw_rect(theme.enemies, move.final.row, move.final.col)
                else:
                    color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                    center_x = move.final.col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = move.final.row * SQUARE_SIZE + SQUARE_SIZE // 2
                    radius = SQUARE_SIZE // 6
                    pygame.draw.circle(self.surface, color, (center_x, center_y), radius)

    def display_last_move(self):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                self.draw_rect(theme.trace, pos.row, pos.col)

    def change_theme(self):
        self.config.change_theme()

    def reset(self):
        self.__init__(self.surface)

    def move_capture_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_self_sound.play()

    def illegal_sound(self):
        self.config.illegal_sound.play()

    