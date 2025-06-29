import pygame

class Sound:
    
    #initialize a path and a sound file for the Sound object
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
    
    #method to play the sound file of the Sound object 
    def play(self):
        pygame.mixer.Sound.play(self.sound)