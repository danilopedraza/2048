from enum import IntEnum
from random import choices, randint

def rot90(m, k=1):
    res = m + []
    for _ in range(k):
        res = [[res[j][i] for j in range(len(res))] for i in range(len(res[0])-1,-1,-1)]
    return res


class GameOf2048:
    class Move(IntEnum):
        # number of move = number of left rotations to 'transform' it to a left move
        LEFT = 0
        UP = 1
        RIGHT = 2
        DOWN = 3

    def __init__(self):
        self.lost = False
        self.moves = 0
        self.points = 0
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
            
            res[x][y] = choices([1,2],[9,1])[0]
        
        return res
    
    def verifyLoss(self):
        if any(0 in row for row in self.currentBoard):
            # there are empty spaces, so we can move
            return False
        else:
            # check for all possible moves
            for i in range(3):
                for j in range(3):
                    down = self.currentBoard[i][j] == self.currentBoard[i+1][j]
                    right = self.currentBoard[i][j] == self.currentBoard[i][j+1] 
                    if down or right:
                        return False
            
            for i in range(3):
                down  = self.currentBoard[i][3] == self.currentBoard[i+1][3]
                right = self.currentBoard[3][i] == self.currentBoard[3][i+1]
                if down or right:
                    return False
            
            return True # no possble moves, game lost

    def transform(self, board):
        # shifts all non-zeros to the side
        for i in range(4):
            done = False
            while not done:
                for j in range(3):
                    if j+1 == 3 and board[i][j+1] == 0:
                        done = True
                        break
                    
                    if board[i][j] == 0 and board[i][j+1] == 0:
                        continue # search nonzeros further
                    elif board[i][j] == 0 and board[i][j+1] != 0:
                        # make a shift, not done yet
                        board[i][j] = board[i][j+1]
                        board[i][j+1] = 0
                        break
                    elif board[i][j] != 0 and board[i][j+1] == 0:
                        continue # nothing to do
                    else: # board[i][j] != 0 and board[i][j+1] != 0
                        continue # nothing to do      

        # makes a merge
        for i in range(4):
            merged = False
            for j in range(3):
                if board[i][j] == board[i][j+1] and board[i][j] != 0 and not merged:
                    # a possible merge was found
                    board[i][j] += 1
                    board[i][j+1] = 0
                    newPoints = 1 << board[i][j] # = 2**board[i][j]

                    self.points += newPoints
                elif merged:
                    # two cells merged and now we have to shift left the ones in the right
                    board[i] = board[i][j+1]
                else:
                    # no past merge and no case for new merge, nothing to do
                    pass
            
            if merged:
                # since the only possible cell without a value is the last,
                # we put it to zero in any case of merge
                board[i][3] = 0
        
        # shifts all non-zeros to the side
        for i in range(4):
            done = False
            while not done:
                for j in range(3):
                    if j+1 == 3 and board[i][j+1] == 0:
                        done = True
                        break
                    
                    if board[i][j] == 0 and board[i][j+1] == 0:
                        continue # search nonzeros further
                    elif board[i][j] == 0 and board[i][j+1] != 0:
                        # make a shift, not done yet
                        board[i][j] = board[i][j+1]
                        board[i][j+1] = 0
                        break
                    elif board[i][j] != 0 and board[i][j+1] == 0:
                        continue # nothing to do
                    else: # board[i][j] != 0 and board[i][j+1] != 0
                        continue # nothing to do
        
    def playMove(self, dir):
        assert type(dir) is self.Move
        if self.lost:
            return False

        # get a new board with the new move
        res = rot90(self.currentBoard, k=int(dir))

        self.transform(res)
        
        res = rot90(res, k=(4-int(dir))%4)
        
        # add a new positive cell
        if res != self.currentBoard:
            # we moved the board, so there is always a zero cell
            x, y = randint(0,3), randint(0,3)
            while res[x][y] != 0:
                x, y = randint(0,3), randint(0,3)
            res[x][y] = choices([1,2],[9,1])[0]

            # update everything
            self.lastBoard = self.currentBoard
            self.currentBoard = res
            self.moves += 1
            self.lost = self.verifyLoss()
                
            return True
        else:
            return False
