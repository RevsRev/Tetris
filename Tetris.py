"""Code to play the game 'Tetris'"""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import copy
import math

#game_height = 20
#game_width = 10
#grid = np.zeros(20,10)

class tetromino:
    
    #Might need to add 'null tetrominoes' here later
    Oshape = np.array([[1,1],[1,1]]) #Yellow
    Tshape = np.array([[0,0,0],[2,2,2],[0,2,0]]) #Purple
    Ishape = np.array([[0,0,0,0],[3,3,3,3],[0,0,0,0],[0,0,0,0]]) #Cyan
    Lshape = np.array([[0,0,0],[4,4,4],[0,0,4]]) #Orange
    Jshape = np.array([[0,0,0], [5,5,5], [5,0,0]]) #Blue
    Sshape = np.array([[0,0,0],[6,6,0],[0,6,6]]) #Green
    Zshape = np.array([[0,0,0],[0,7,7],[7,7,0]]) #Red
    
    def __init__(self, grid, board_location):
        #grid is an np array that encodes the structure of the Tetromino.
        #board location is the location of the tetromino on the game board.
        self.grid = grid
        self.board_location = board_location
    
    def rotate(self):
        #Rotates the array (tetromino) by 90 degrees clockwise (about the
        #centre of the array.)
        _ = np.zeros((self.grid.shape[1], self.grid.shape[0]))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                _[j,self.grid.shape[0]-i-1] = self.grid[i,j]
        self.grid = _
        

class board:
    
    def __init__(self):
        self.height = 22
        self.width = 10
        self.grid = np.zeros((self.height,self.width))
        self.score = 0
        self.level = 1
    
    def add_tetromino_to_board(self, tetro):
        #Adds a tetromino and also removes from behind (to give impression of motion.)
        #Position is top left corner of the tetromino grid
        for i in range(tetro.grid.shape[0]):
            for j in range(tetro.grid.shape[1]):
                if tetro.grid[i][j] != 0:
                    self.grid[tetro.board_location[0]-i][tetro.board_location[1]+j] = tetro.grid[i][j]
                
    def delete_tetro_from_board(self, tetro):
        for i in range(tetro.grid.shape[0]):
            for j in range(tetro.grid.shape[1]):
                if tetro.grid[i,j]!=0:
                    self.grid[tetro.board_location[0]-i][tetro.board_location[1]+j] = 0
                
    def testing(self, tetro, tet_dir):
        if tet_dir == 'left':
            for i in range(tetro.grid.shape[0]):
                print(i)
    
    def move_tetro_on_board(self, tetro, tet_dir):
        #Moves the tetrominoes around and acts as collision detector (returns
        #1 if a collision, moves tetromino and returns 0 otherwise)
        if tet_dir == "left":
            for i in range(tetro.grid.shape[0]):
                j=0
                while j<tetro.grid.shape[1] and  tetro.grid[i][j] ==0:
                    j=j+1
                if j<tetro.grid.shape[1]:
                    if tetro.board_location[1]+j==0 or \
                    self.grid[tetro.board_location[0] - i][tetro.board_location[1] + j -1] != 0:
                        return 1
            self.delete_tetro_from_board(tetro)
            tetro.board_location = [tetro.board_location[0], tetro.board_location[1]-1]
            self.add_tetromino_to_board(tetro)
            return 0
        elif tet_dir == "right":
            for i in range(tetro.grid.shape[0]):
                j=tetro.grid.shape[1]-1
                while j>-1 and tetro.grid[i][j] == 0:
                    j = j-1
                if j>-1:
                    if tetro.board_location[1]+j == self.width-1 or \
                    self.grid[tetro.board_location[0]-i][tetro.board_location[1]+j+1] != 0:
                        return 1
            self.delete_tetro_from_board(tetro)
            tetro.board_location = [tetro.board_location[0], tetro.board_location[1]+1]
            self.add_tetromino_to_board(tetro)
            return 0
        elif tet_dir == "down":
            for j in range(tetro.grid.shape[1]):
                i=tetro.grid.shape[0]-1
                while i>-1 and tetro.grid[i][j] == 0:
                    i=i-1
                if i>-1:
                    if tetro.board_location[0]-i == 0 or \
                    self.grid[tetro.board_location[0]-i-1][tetro.board_location[1]+j] !=0:
                        return 1
            self.delete_tetro_from_board(tetro)
            tetro.board_location = [tetro.board_location[0]-1, tetro.board_location[1]]
            self.add_tetromino_to_board(tetro)
            return 0
        elif tet_dir == "up":
            try:
                tetro2 = copy.deepcopy(tetro)
                tetro2.rotate()
                for i in range(tetro2.grid.shape[0]):
                    for j in range(tetro2.grid.shape[1]):
                        if tetro.grid[i][j] == 0:
                            if self.grid[tetro.board_location[0]-i][tetro.board_location[1]+j] != 0:
                                return 1
                            if tetro.board_location[1]+j <0:
                                raise IndexError
                self.delete_tetro_from_board(tetro)
                del tetro2
                tetro.rotate()
                self.add_tetromino_to_board(tetro)
                return 0
            except IndexError:
                _ = self.move_tetro_on_board(tetro,"left")
                if _ == 1:
                    _ = self.move_tetro_on_board(tetro,"right")
                    if _ ==1:
                        return 1
                self.move_tetro_on_board(tetro, "up")

            
    def scan_and_update(self):
        for i in range(self.height):
            clear_row = 0
            for j in range(self.width):
                if self.grid[self.height-i-1,j]==0:
                    clear_row = 1
            if clear_row == 0:
                self.grid = np.delete(self.grid, self.height -1 - i, 0)
                self.grid = np.vstack([self.grid, np.zeros((1,10))])
                self.score = self.score+1
            
       
def plot(board, fig, ax):
    plt.cla()
    cmap = colors.ListedColormap(['black', 'grey', 'yellow', 'purple', 'cyan','orange','blue','green','red'])
    bounds = [-1,-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    
    ax.imshow(board.grid, cmap = cmap, norm = norm)
    
    ax.grid(which = 'major', axis = 'both', linestyle = '-', color = 'k', linewidth = 2)
    ax.set_xlim(-0.5,9.5)
    ax.set_ylim(-0.5,19.5)
    ax.set_xticks(np.arange(-.5, 10, 1));
    ax.set_yticks(np.arange(-.5, 20, 1));
    plt.title("Tetris!\nLevel: " + str(board.level) + " Score: " + str(board.score))
    
    frame = plt.gca()
    frame.axes.xaxis.set_ticklabels([])
    frame.axes.yaxis.set_ticklabels([])
    #plt.pause(0.2)

def on_press(event):
    global tet_dir, game_state
    tet_dir = event.key
    if event.key == 'escape':
        plt.close()
        game_state =1
        
def on_release(event):
    global tet_dir, game_state
    tet_dir = ""

def play_tetris():
    global tet_dir, game_state
    tet_dir = ""
    game_state = 0
    brd = board()
    fig, ax = plt.subplots()
    plot(brd,fig,ax)
    cidpress = fig.canvas.mpl_connect('key_press_event',on_press)
    cidrelease = fig.canvas.mpl_connect('key_release_event', on_release)
    tetromino_array = [tetromino.Oshape, tetromino.Tshape, tetromino.Ishape, tetromino.Lshape,
                   tetromino.Jshape, tetromino.Zshape, tetromino.Sshape]
    while game_state ==0:
        brd.level = math.floor(brd.score/10)+1
        tetro = tetromino(np.random.choice(tetromino_array), [brd.height-1,4])
        brd.add_tetromino_to_board(tetro)
        plt.pause(0.05)
        while (brd.move_tetro_on_board(tetro, tet_dir)!=1 or tet_dir != "down") and game_state==0:
            tet_dir = ""
            time = 0
            T = 0.3/(math.sqrt(brd.level))
            while time<T and game_state == 0:
                brd.move_tetro_on_board(tetro, tet_dir)
                plot(brd,fig,ax)
                plt.pause(0.03)
                time = time + 0.03
            tet_dir = 'down'
        brd.scan_and_update()
        if tetro.board_location[0]>=19:
            game_state=1
            print("GAME OVER.\nYou reached level: " + str(brd.level) + "\nYou scored: " + str(brd.score))
            plt.close()
    fig.canvas.mpl_disconnect(cidpress)
    fig.canvas.mpl_disconnect(cidrelease)