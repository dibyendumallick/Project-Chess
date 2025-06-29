from game.scripts.config.Sound import Sound
from game.scripts.config.Theme import Theme
from game.scripts.Constants import *

import pygame
import os

class Config:
    
    def __init__(self):
        self.add_sounds()                                               #add all defined sounds
        self.themes = []                                                #list of possible themes
        self.add_theme()                                                #add all defined themes
        self.index = 0                                                  #index for themes, default set to 0
        self.theme = self.themes[self.index]                            #theme set to themes[index]
        self.font = pygame.font.SysFont('monospace', 14, bold=True)     #font for row and col labels
    
    #method to change themes
    def change_theme(self):
        self.index += 1                         #incrementing index
        self.index %= len(self.themes)          #prevents out of bounds error
        self.theme = self.themes[self.index]    #sets the theme according to the index
    
    #adds all sound files, as Sound objects
    def add_sounds(self): 
        base_sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/sounds"))
        self.capture_sound = Sound(os.path.join(base_sound_path, "capture.wav"))
        self.castle_sound = Sound(os.path.join(base_sound_path, "castle.wav"))
        self.game_end_sound = Sound(os.path.join(base_sound_path, "game_end.wav"))
        self.game_start_sound = Sound(os.path.join(base_sound_path, "game_start.wav"))
        self.illegal_sound = Sound(os.path.join(base_sound_path, "illegal.wav"))
        self.move_check_sound = Sound(os.path.join(base_sound_path, "move_check.wav"))
        self.move_self_sound = Sound(os.path.join(base_sound_path, "move_self.wav"))
        self.notify_sound = Sound(os.path.join(base_sound_path, "notify.wav"))
        self.premove_sound = Sound(os.path.join(base_sound_path, "premove.wav"))
        self.promote_sound = Sound(os.path.join(base_sound_path, "promote.wav"))
        self.ten_seconds_sound = Sound(os.path.join(base_sound_path, "ten_seconds.wav"))
    
    #adds all themes, with colors defined in Constants class
    def add_theme(self):
        green = Theme(GREEN_LIGHT, GREEN_DARK, GREEN_TRACE_LIGHT, GREEN_TRACE_DARK, GREEN_MOVE_LIGHT, GREEN_MOVE_DARK, LIGHT_RED, DARK_RED)
        brown = Theme(BROWN_LIGHT, BROWN_DARK, BROWN_TRACE_LIGHT, BROWN_TRACE_DARK, BROWN_MOVE_LIGHT, BROWN_MOVE_DARK, LIGHT_RED, DARK_RED)
        blue = Theme(BLUE_LIGHT, BLUE_DARK, BLUE_TRACE_LIGHT, BLUE_TRACE_DARK, BLUE_MOVE_LIGHT, BLUE_MOVE_DARK, LIGHT_RED, DARK_RED) 
        gray = Theme(GRAY_LIGHT, GRAY_DARK, GRAY_TRACE_LIGHT, GRAY_TRACE_DARK, GRAY_MOVE_LIGHT, GRAY_MOVE_DARK, LIGHT_RED, DARK_RED)
        
        self.themes = [green, brown, blue, gray]