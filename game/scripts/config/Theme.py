from game.scripts.config.Color import Color

class Theme:
    
    #initialize themes with background, last move(trace), valid moves, and enemy square colors (all taken from Constants class)
    def __init__(self, light_bg, dark_bg, light_trace, dark_trace, light_moves, dark_moves, light_enemy, dark_enemy):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
        self.enemies = Color(light_enemy, dark_enemy)