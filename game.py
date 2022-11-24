from enum import Enum
from random import randint

def rot90(m, k=1):
    res = []
    for _ in range(k):
        res = [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
    return res


class GameOf2048:
    class Move(Enum):
        # number of move = number of left rotations to 'transform' it to a left move
        LEFT = 0
        UP = 1
        RIGHT = 2
        DOWN = 3

    def __init__(self):
        self.moves = 0
        self.lastBoard = None
        self.currentBoard = self.initialBoard()
    
    def initialBoard(self):
        res = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
        
        for _ in range(2):
            x, y = randint(0,3), randint(0,3)
            while res[x][y] != 0:
                x, y = randint(0,3), randint(0,3)
            
            res[x][y] = randint(1,2)
        
        return res
    
    def notLost(self):
        pass # TODO: verify the game can continue

    def transform(self, row):
        merged = False
        for i in range(len(row)-1):
            if row[i] == row[i+1] and row[i] != 0 and not merged:
                # a possible merge was found
                row[i] += 1
            elif merged:
                # two cells merged and now we have to shift left the ones in the right
                row[i] = row[i+1]
            else:
                # no past merge and no case for new merge, nothing to do
                pass
        
        if merged:
            # since the only possible cell without a value is the last,
            # we put it to zero in any case of merge
            row[len(row)-1] = 0
    
    def playMove(self, dir):
        assert type(dir) is self.Move

        res = rot90(self.currentBoard, k=int(dir))

        for row in res:
            self.transform(row)
        
        res = rot90(res, k=(4-int(dir))%4)
        
        if res != self.currentBoard:
            x, y = randint(0,3), randint(0,3)

            if self.notLost():
                while res[x][y] != 0:
                    x, y = randint(0,3), randint(0,3)
                res[x][y] = randint(1,2)

            self.lastBoard = self.currentBoard
            self.currentBoard = res
            
            return True
        else:
            return False



# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("2048")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((400,400))
    
    # define a variable to control the main loop
    running = True
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
