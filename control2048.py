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
    def Up(self):
        time.sleep(self.sleepTime)
        self.action.send_keys(Keys.ARROW_UP)
        self.__perform("Up")
    def Down(self):
        time.sleep(self.sleepTime)
        self.action.send_keys(Keys.ARROW_DOWN)
        self.__perform("Down")
    def Right(self):
        time.sleep(self.sleepTime)
        self.action.send_keys(Keys.ARROW_RIGHT)
        self.__perform("Right")
    def Left(self):
        time.sleep(self.sleepTime)
        self.action.send_keys(Keys.ARROW_LEFT)
        self.__perform("Left")
    def __perform(self, movement):
        if self.verbose:
            print(movement)
        self.action.perform()
mov = Control()
mov.Up()
mov.Down()
mov.Right()
mov.Left()
