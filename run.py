import sys
import os

# Add the game directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#add Main class
from game.scripts.Main import Main

#call run method of Main class
main = Main()
main.run()