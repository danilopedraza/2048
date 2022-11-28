from game import GameOf2048

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time


class Control:
    def __init__(self, sleepTime = 1, verbose = False):
        self.sleepTime = sleepTime
        self.verbose = verbose

        self.driver = webdriver.Firefox()
        self.driver.get("https://2048game.com")
        
        self.action = ActionChains(self.driver)

        self.dirs = {
            GameOf2048.Move.LEFT : (Keys.ARROW_LEFT , 'Down' ),
            GameOf2048.Move.UP   : (Keys.ARROW_UP   , 'Up'   ),
            GameOf2048.Move.RIGHT: (Keys.ARROW_RIGHT, 'Right'),
            GameOf2048.Move.DOWN : (Keys.ARROW_DOWN , 'Left' ),
        }
    
    def pressArrow(self, dir):
        assert type(dir) is GameOf2048.Move

        time.sleep(self.sleepTime)
        self.action.send_keys(self.dirs[dir][0])
        self.__perform(self.dirs[dir][1])
    
    def __perform(self, movement):
        if self.verbose:
            print(movement)
        self.action.perform()



if __name__ == '__main__':
    mov = Control()
    moves = [
        GameOf2048.Move.UP,
        GameOf2048.Move.DOWN,
        GameOf2048.Move.RIGHT,
        GameOf2048.Move.LEFT,
    ]
    
    for dir in moves:
        mov.pressArrow(dir)
