import logging
from game_logic.PlayerInterface import PlayerInterface

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("__main__.py").info("Project has run")
    #Add your logic here
    PlayerInterface()
