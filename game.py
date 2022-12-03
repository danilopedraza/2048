from enum import IntEnum
from gym import Env
from gym.spaces import Box, Discrete
import numpy as np
from random import choices, randint
import random



class GameOf2048(Env):
    class Move(IntEnum):
        # number of move = number of left rotations to 'transform' it to a left move
        LEFT = 0
        UP = 1
        RIGHT = 2
        DOWN = 3

    def __init__(self, seed=None):
        if seed: # != None:
            random.seed(seed)
        else:
            pass

        self.lost = False
        self.moves = 0
        self.currentBoard = self.initialBoard()

        # attributes for the Env superclass
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0 ,high=3, shape=(4,4), dtype=np.uint32)
        self.reward_range = (0, np.inf)


    # helper functtions for game logic
    def initialBoard(self):
        res = np.asarray([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ], dtype=np.uint32)
        
        
        for _ in range(2):
            x, y = randint(0,3), randint(0,3)
            while res[x,y] != 0:
                x, y = randint(0,3), randint(0,3)
            
            res[x,y] = choices([2,4],[9,1])[0]
        
        return res
    
    def verifyLoss(self):
        if 0 in self.currentBoard:
            # there are empty spaces, so we can move
            return False
        else:
            # check for all possible moves
            for i in range(3):
                for j in range(3):
                    down = self.currentBoard[i,j] == self.currentBoard[i+1,j]
                    right = self.currentBoard[i,j] == self.currentBoard[i,j+1]
                    if down or right:
                        return False
            
            for i in range(3):
                down  = self.currentBoard[i,3] == self.currentBoard[i+1,3]
                right = self.currentBoard[3,i] == self.currentBoard[3,i+1]
                if down or right:
                    return False
            
            return True # no possible moves, game lost
    
    def shiftEverythingLeft(self, board):
        # shifts all non-zeros to the side
        for i in range(4):
            for j in range(4):
                if board[i,j] == 0:
                    for k in range(j+1,4):
                        if board[i,k] != 0:
                            board[i,j] = board[i,k]
                            board[i,k] = 0
                            break
                        else:
                            continue
                else:
                    continue

    def transform(self, board):
        pointsEarned = 0

        self.shiftEverythingLeft(board)

        # makes a merge
        for i in range(4):
            merged = False
            for j in range(3):
                if board[i,j] == board[i,j+1] and board[i,j] != 0 and not merged:
                    # a possible merge was found
                    board[i,j] *= 2
                    board[i,j+1] = 0

                    pointsEarned += board[i,j]
                elif merged:
                    # two cells merged and now we have to shift left the ones in the right
                    board[i,j] = board[i,j+1]
                else:
                    # no past merge and no case for new merge, nothing to do
                    pass
            
            if merged:
                # since the only possible cell without a value is the last,
                # we put it to zero in any case of merge
                board[i,3] = 0

        self.shiftEverythingLeft(board)
        
        return pointsEarned
    


    # functions for the Env superclass
    def step(self, dir):
        # get a new board with the new move
        # dir is an int
        res = np.rot90(np.copy(self.currentBoard), k=dir)

        pointsEarned = self.transform(res)
        
        res = np.rot90(res, k=(4-dir)%4)

        # add a new positive cell
        if not np.array_equal(res, self.currentBoard):
            # we moved the board, so there is always a zero cell
            x, y = randint(0,3), randint(0,3)
            while res[x,y] != 0:
                x, y = randint(0,3), randint(0,3)
            res[x,y] = choices([2,4],[9,1])[0]

            self.currentBoard = res
            self.moves += 1
            self.lost = self.verifyLoss()
        else:
            pass # nothing to update, no tile to add
        
        return (
            self.currentBoard, # the new board (if changed)
            np.float(pointsEarned), # points earned (can be zero)
            self.lost, # the game ended?
            False, # the game was truncated (limit of steps)?
            {} # information of the step
        )
    
    def reset(self):
        self.lost = False
        self.moves = 0
        self.currentBoard = self.initialBoard()

        return (
            self.currentBoard,
            {} # for information
        )
    
    def render(self):
        pass
