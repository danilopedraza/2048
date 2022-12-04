from game import GameOf2048

import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time


class Control:
    def __init__(self, sleepTime = 1, verbose = False):
        self.sleepTime = sleepTime
        self.verbose = verbose

        self.driver = webdriver.Firefox()
        self.driver.get('https://danilopedraza.github.io/2048-port/')
        
        self.action = ActionChains(self.driver)

        self.dirs = {
            GameOf2048.Move.LEFT : (Keys.ARROW_LEFT , 'Left' ),
            GameOf2048.Move.UP   : (Keys.ARROW_UP   , 'Up'   ),
            GameOf2048.Move.RIGHT: (Keys.ARROW_RIGHT, 'Right'),
            GameOf2048.Move.DOWN : (Keys.ARROW_DOWN , 'Down' ),
        }

        self.dirs = [
            (Keys.ARROW_LEFT , 'Left' ),
            (Keys.ARROW_UP   , 'Up'   ),
            (Keys.ARROW_RIGHT, 'Right'),
            (Keys.ARROW_DOWN , 'Down' ),
        ]

        time.sleep(1) # wait for the page to load
        self.tilesHTML = self.driver.find_element(
            By.CLASS_NAME,
            'tile-container'
        ) # div with tiles
        self.updateGrid()

        # self.currentGrid gets initialized in self.updateGrid()
    
    def pressArrow(self, dir):
        # assert type(dir) is GameOf2048.Move

        time.sleep(self.sleepTime)
        self.action.send_keys(self.dirs[dir][0])
        self.__perform(self.dirs[dir][1])
        self.updateGrid()
    
    def __perform(self, movement):
        if self.verbose:
            print(movement)
            print(self.currentGrid)
        self.action.perform()

    
    def parseTileClassName(self, classname):
        # the info of a tile is in its div classname
        # the names are of the form
        # tile tile-[1-9][0-9]* tile-position-[1-4]-[1-4] (tile-new|tile-merged|)
        arr = classname.split(' ')
        number = arr[1].split('-')
        position = arr[2].split('-')
        if len(arr) > 3:
            state = arr[3].split('-')[-1]
        else:
            state = None
        
        return {
            'number': number[1],
            'position': {
                # inverted coordinates (xy-plane order to matrix order)
                'x': position[3],
                'y': position[2]
            },
            'state': state
        }

    def getGridFromTiles(self, tiles):
        # after a merge, the previous cells are still in the div
        # this method takes care of that
        tileGroups = {}
        for tile in tiles:
            key = str(tile['position'])
            if key in tileGroups:
                tileGroups[key].append(tile)
            else:
                tileGroups[key] = [tile]
        
        res = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
        ]

        for coord in tileGroups:
            group = tileGroups[coord]

            if len(group) == 1:
                tile = group[0]
                x = int(tile['position']['x'])-1
                y = int(tile['position']['y'])-1
                res[x][y] = int(tile['number'])
            else: # len(group) > 1
                for tile in group:
                    if tile['state'] == 'merged':
                        x = int(tile['position']['x'])-1
                        y = int(tile['position']['y'])-1
                        res[x][y] = int(tile['number'])
                    else:
                        continue

        return res
    

    def updateGrid(self):
        time.sleep(0.5) # make sure the page updates the DOM after playing
        children = self.tilesHTML.find_elements(By.TAG_NAME, 'div')
        tiles = (self.parseTileClassName(element.get_attribute('class'))
                    for element in children
                    if element.get_attribute('class') != 'tile-inner'
                )
        
        self.currentGrid = np.asarray(self.getGridFromTiles(tiles))
